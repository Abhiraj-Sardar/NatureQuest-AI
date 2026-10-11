const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
async function request(path, body) {
  let response;
  try { response = await fetch(`${BASE}${path}`, {method:body ? "POST":"GET", headers:body?{"Content-Type":"application/json"}:undefined, body:body?JSON.stringify(body):undefined}); }
  catch { throw new Error("Cannot reach local backend. Start FastAPI at http://localhost:8000."); }
  const data = await response.json().catch(()=>({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}
export const getHealth = () => request("/health");
export const generateQuest = (settings) => request("/api/quest", settings);
export const askNaturalist = (payload) => request("/api/ask", payload);
