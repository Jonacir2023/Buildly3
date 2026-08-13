// Buildly — cliente Supabase
// Chave "publishable/anon" é segura para uso no front-end: o acesso real aos
// dados é controlado por Row Level Security (RLS) nas tabelas, não pela chave.
//
// A biblioteca (js/vendor/supabase.js) cria o global `supabase` (namespace);
// o cliente da aplicação se chama `db` para não colidir com esse nome.

const SUPABASE_URL = "https://hvaiqfbtgumxygdsnqgl.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_wmGD5fTQvWBOMW3M5aSxbw_y9e0Bd1u";

var db = null;
if (window.supabase && typeof window.supabase.createClient === "function") {
  db = window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);
}
