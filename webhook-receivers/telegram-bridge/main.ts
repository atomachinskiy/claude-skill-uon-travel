// U-On → Telegram bridge.
// Минимальный receiver, работает как Cloudflare Worker, Deno Deploy или Vercel Edge.

const EVENT_NAMES: Record<number, string> = {
  1: "Создание обращения",
  2: "Создание заявки",
  3: "Создание клиента",
  4: "Изменение клиента",
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
};

interface Env {
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_CHAT_ID: string;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);

    if (req.method === "GET" && url.pathname === "/health") {
      return new Response("ok", { status: 200 });
    }

    let payload: Record<string, string> = {};
    if (req.method === "POST") {
      const ct = req.headers.get("content-type") || "";
      if (ct.includes("json")) {
        payload = (await req.json()) as Record<string, string>;
      } else {
        const body = await req.text();
        payload = Object.fromEntries(new URLSearchParams(body));
      }
    } else {
      payload = Object.fromEntries(url.searchParams);
    }

    const typeId = parseInt(payload.type_id, 10);
    const eventName = EVENT_NAMES[typeId] || `Событие #${typeId}`;

    const lines = [`🔔 *U-On: ${esc(eventName)}* \\(type=${typeId}\\)`];
    if (payload.request_id) lines.push(`📋 Заявка \\#${esc(payload.request_id)}`);
    if (payload.client_id) lines.push(`👤 Клиент \\#${esc(payload.client_id)}`);
    if (payload.tourist_id && !payload.client_id) lines.push(`👤 Турист \\#${esc(payload.tourist_id)}`);
    if (payload.status_old && payload.status_new) lines.push(`📊 ${esc(payload.status_old)} → ${esc(payload.status_new)}`);
    if (payload.price) lines.push(`💰 ${esc(payload.price)} ₽`);
    if (payload.summa) lines.push(`💰 ${esc(payload.summa)} ₽`);
    if (payload.text) lines.push(`💬 ${esc(payload.text.slice(0, 300))}`);
    if (payload.uon_subdomain) {
      lines.push(`🔗 [Открыть кабинет](https://${esc(payload.uon_subdomain)}\\.u\\-on\\.ru)`);
    }
    const text = lines.join("\n");

    try {
      await fetch(
        `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: env.TELEGRAM_CHAT_ID,
            text,
            parse_mode: "MarkdownV2",
            disable_web_page_preview: true,
          }),
        },
      );
    } catch (e) {
      console.error("TG forward failed", e);
    }

    return new Response(JSON.stringify({ ok: true, typeId, eventName }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
};

function esc(s: string): string {
  return String(s).replace(/([_*[\]()~`>#+\-=|{}.!])/g, "\\$1");
}
