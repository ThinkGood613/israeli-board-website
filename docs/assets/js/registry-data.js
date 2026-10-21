// SAMPLE DATA ONLY — fictional records for demonstrating the registry search.
// Replace with an export from the Board's credentialing database (or an API call)
// before launch. Fields: name_he, name_en, credential, endorsements, number,
// city_he, city_en, expires (YYYY-MM-DD), status: active | expired | inactive.
window.REGISTRY = [
  { name_he: "דוגמה ישראלי", name_en: "Sample Israeli", credential: "MAC", endorsements: ["GD-E"], number: "IL-10001", city_he: "תל אביב-יפו", city_en: "Tel Aviv-Yafo", expires: "2027-12-31", status: "active" },
  { name_he: "נועה לדוגמה", name_en: "Noa Example", credential: "CAC II", endorsements: [], number: "IL-10002", city_he: "חיפה", city_en: "Haifa", expires: "2027-06-30", status: "active" },
  { name_he: "סמיר דוגמה", name_en: "Samir Sample", credential: "CAC I", endorsements: [], number: "IL-10003", city_he: "נצרת", city_en: "Nazareth", expires: "2026-03-31", status: "expired" },
  { name_he: "דנה מבחן", name_en: "Dana Test", credential: "CCS", endorsements: ["CSB-E", "COD-E"], number: "IL-10004", city_he: "ירושלים", city_en: "Jerusalem", expires: "2028-01-31", status: "active" },
  { name_he: "יוסי דמה", name_en: "Yossi Demo", credential: "CAC II", endorsements: ["DIG-E"], number: "IL-10005", city_he: "באר שבע", city_en: "Be'er Sheva", expires: "2027-09-30", status: "active" },
  { name_he: "מרים פלונית", name_en: "Miriam Ploni", credential: "MAC", endorsements: [], number: "IL-10006", city_he: "רמת גן", city_en: "Ramat Gan", expires: "2026-12-31", status: "inactive" }
];
