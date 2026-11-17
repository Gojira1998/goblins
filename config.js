/* Loja dos goblins (Ko-fi). Trocar os dois marcadores pelos links das encomendas no Ko-fi quando a loja existir.
   Enquanto começar com "KOFI_", os botões aparecem como "Shop opens soon" e não levam a lugar nenhum (dá pra publicar sem quebrar nada).
   Exemplo: hd: "https://ko-fi.com/agentsgoblins/commissions"  (passo a passo em escritorio-jga/relatorios/conta-C-loja-pronta.md) */
window.GOBLIN_SHOP = {
  hd: "KOFI_HD_URL",          // "Your Goblin HD", US$ 3
  anim: "KOFI_ANIM_URL",      // "Animated Goblin", US$ 7
  priceHd: "$3",
  priceAnim: "$7",
  // goblins que não vão pra venda: personagem de marca ou @ com palavra ofensiva (sem o @ e em minúsculas)
  block: ["wayne_p_mckie", "rivertheretard"]
};
