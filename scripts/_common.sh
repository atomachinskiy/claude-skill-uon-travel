#!/usr/bin/env bash
# _common.sh — общие функции для U-On API shell-обёрток.
# Все скрипты source'ят этот файл.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Загрузка .env (если есть)
if [[ -f "$REPO_ROOT/config/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$REPO_ROOT/config/.env"
    set +a
fi

# Fallback на серверный secret-файл (для Андрея на claude5)
if [[ -z "${UON_API_KEY:-}" ]] && [[ -f "$HOME/.claude/secrets/uon-api-key" ]]; then
    UON_API_KEY="$(cat "$HOME/.claude/secrets/uon-api-key")"
fi

if [[ -z "${UON_API_KEY:-}" ]]; then
    echo "❌ UON_API_KEY не задан. Положи ключ в config/.env или ~/.claude/secrets/uon-api-key" >&2
    exit 1
fi

UON_FORMAT="${UON_FORMAT:-json}"
UON_TIMEOUT="${UON_TIMEOUT:-30}"
UON_THROTTLE_MS="${UON_THROTTLE_MS:-150}"
UON_BASE="https://api.u-on.ru/${UON_API_KEY}"

# uon_get <endpoint-without-format>
# пример: uon_get "manager" → GET https://api.u-on.ru/{KEY}/manager.json
uon_get() {
    local ep="$1"
    local url="${UON_BASE}/${ep}.${UON_FORMAT}"
    _uon_throttle
    curl -sS -G --max-time "$UON_TIMEOUT" "$url"
}

# uon_post <endpoint-without-format> [k=v ...]
# пример: uon_post "user/create" "u_name=Иван" "u_phone_mobile=+79..."
uon_post() {
    local ep="$1"
    shift
    local url="${UON_BASE}/${ep}.${UON_FORMAT}"
    _uon_throttle
    local data_args=()
    for kv in "$@"; do
        data_args+=(--data-urlencode "$kv")
    done
    curl -sS --max-time "$UON_TIMEOUT" -X POST "$url" "${data_args[@]}"
}

# uon_pretty — pipe JSON через python для красивого вывода
uon_pretty() {
    if command -v jq >/dev/null 2>&1; then
        jq .
    else
        python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), ensure_ascii=False, indent=2))"
    fi
}

# Внутренний rate-limit (sleep)
_uon_throttle() {
    if [[ "$UON_THROTTLE_MS" -gt 0 ]]; then
        local sec
        sec=$(awk "BEGIN {printf \"%.3f\", $UON_THROTTLE_MS/1000}")
        sleep "$sec"
    fi
}

# Проверить что результат не ошибка (по полю result)
uon_check_ok() {
    local resp="$1"
    if python3 -c "import sys,json; d=json.loads('''$resp'''); sys.exit(0 if d.get('result',200)==200 else 1)" 2>/dev/null; then
        return 0
    fi
    echo "❌ U-On вернул ошибку:" >&2
    echo "$resp" | uon_pretty >&2
    return 1
}
