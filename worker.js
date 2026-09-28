export default {
  async fetch() {
    try {
      const r = await fetch(
        "https://torgi.gov.ru/new/opendata/7710568760-notice/data-20260927T0000-20260928T0000-structure-20240401.json"
      );

      return new Response("STATUS: " + r.status);
    } catch (e) {
      return new Response("ERROR: " + e);
    }
  }
};