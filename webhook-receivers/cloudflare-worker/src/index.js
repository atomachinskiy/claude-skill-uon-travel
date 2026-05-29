// Cloudflare Worker — U-On.Travel webhook receiver.
// Принимает POST/GET, парсит payload, форвардит в TG/общий URL/KV.

const EVENT_NAMES = {
  1: "Создание обращения",
  2: "Создание заявки",
  3: "Создание клиента",
  4: "Изменение клиента",
  5: "Удаление клиента",
  9: "Создание платежа",
  10: "Изменение платежа",
  12: "Создание услуги в заявке",
  16: "Изменение статуса в обращении",
  17: "Изменение статуса в заявке",
  22: "Добавление туриста в заявке",
  31: "Добавление комментария",
  34: "Добавление задачи",
  40: "Изменение статуса в заявке (по оплате)",
  44: "Удаление заявки",
  46: "Создание счёта на оплату",
  59: "Изменение планового платежа на оплаченный",
  61: "Клик по номеру телефона клиента",
  63: "Пропущенный звонок по телефонии",
  // ... полный список 69 типов — в references/webhook-events.md
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === "GET" && new URL(request.url).pathname === "/health") {
      return new Response("ok", { status: 200 });
    }

    // U-On шлёт GET с query-string (default) или POST с form-encoded body
    let payload = {};
    const ct = request.headers.get("content-type") || "";
    if (request.method === "POST") {
      if (ct.includes("application/json")) {
        payload = await request.json();
      } else {
        const body = await request.text();
        payload = Object.fromEntries(new URLSearchParams(body));
      }
    } else {
      payload = Object.fromEntries(new URL(request.url).searchParams);
    }

    const typeId = parseInt(payload.type_id, 10);
    const eventName = EVENT_NAMES[typeId] || `Событие #${typeId}`;
    const uonId = payload.uon_id;
    const dt = payload.datetime;

    // 1) KV: лог последних 100 событий (опц.)
    if (env.UON_LOGS) {
      const key = `event:${Date.now()}:${typeId}`;
      ctx.waitUntil(
        env.UON_LOGS.put(key, JSON.stringify({ typeId, eventName, uonId, dt, payload }), {
          expirationTtl: 60 * 60 * 24 * 7,  // 7 days
        })
      );
    }

    // 2) Telegram-форвард (опц.)
    if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
      const text = formatForTelegram(typeId, eventName, payload);
      ctx.waitUntil(sendToTelegram(env, text));
    }

    // 3) Общий webhook-форвард (опц.)
    if (env.FORWARD_WEBHOOK_URL) {
      ctx.waitUntil(
        fetch(env.FORWARD_WEBHOOK_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ source: "uon-travel", typeId, eventName, payload, receivedAt: new Date().toISOString() }),
        })
      );
    }

    return new Response(JSON.stringify({ ok: true, typeId, eventName }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
};

function formatForTelegram(typeId, eventName, p) {
  const lines = [`🔔 *U-On: ${escapeMd(eventName)}* (type=${typeId})`];
  if (p.request_id) lines.push(`📋 Заявка #${p.request_id}`);
  if (p.client_id || p.tourist_id) lines.push(`👤 Клиент #${p.client_id || p.tourist_id}`);
  if (p.status_old && p.status_new) lines.push(`📊 ${escapeMd(p.status_old)} → ${escapeMd(p.status_new)}`);
  if (p.price || p.summa) lines.push(`💰 ${p.price || p.summa} ₽`);
  if (p.text) lines.push(`💬 ${escapeMd(p.text.slice(0, 300))}`);
  if (p.uon_subdomain) lines.push(`🔗 [Открыть кабинет](https://${p.uon_subdomain}.u-on.ru)`);
  return lines.join("\n");
}

function escapeMd(s) {
  return String(s).replace(/([_*[\]()~`>#+\-=|{}.!])/g, "\\$1");
}

async function sendToTelegram(env, text) {
  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: env.TELEGRAM_CHAT_ID,
      text,
      parse_mode: "MarkdownV2",
      disable_web_page_preview: true,
    }),
  });
}
