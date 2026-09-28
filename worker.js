export default {
  async fetch() {
    try {
      const r = await fetch("https://torgi.gov.ru/opendata/list.json");
      return new Response("STATUS: " + r.status);
    } catch (e) {
      return new Response("ERROR: " + e);
    }
  }
};