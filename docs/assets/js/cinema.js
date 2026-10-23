/* =====================================================================
   SÓ FACHADAS — camada de browser
   - um único loop de requestAnimationFrame (parallax, header, reveal)
   - menu mobile, filtro + lightbox do portfólio, formulário -> WhatsApp
   - sem este arquivo o site continua funcionando (links e WhatsApp)
   ===================================================================== */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  doc.classList.add("js");

  var CFG = window.SF_CONFIG || {};
  var reduz = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var toque = window.matchMedia("(hover: none), (pointer: coarse)").matches;

  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }

  /* ---------- título do hero em cascata ---------- */
  var h1 = $(".hero h1");
  if (h1 && !reduz) {
    $$(".w", h1).forEach(function (w, i) { w.style.transitionDelay = (i * 70) + "ms"; });
    requestAnimationFrame(function () { requestAnimationFrame(function () { h1.classList.add("pronto"); }); });
  }

  /* ---------- reveal: lista pending varrida no loop (não IntersectionObserver) ---------- */
  var pending = [];
  function registraReveal(el) { if (!el.__rv) { el.__rv = true; pending.push(el); } }
  $$(".reveal").forEach(registraReveal);
  if (reduz) { pending.forEach(function (el) { el.classList.add("visto"); }); pending = []; }

  /* MutationObserver: inicializa elementos que surgirem depois */
  new MutationObserver(function (muts) {
    muts.forEach(function (m) {
      m.addedNodes.forEach(function (n) {
        if (n.nodeType !== 1) return;
        if (n.classList.contains("reveal")) registraReveal(n);
        $$(".reveal", n).forEach(registraReveal);
        if (n.classList.contains("lightcard")) ligaLightcard(n);
      });
    });
  }).observe(document.body, { childList: true, subtree: true });

  /* ---------- parallax ---------- */
  var camadas = reduz ? [] : $$("[data-depth]").map(function (el) {
    return { el: el, d: parseFloat(el.getAttribute("data-depth")) || 0 };
  });
  var mouseX = 0, mouseY = 0, alvoX = 0, alvoY = 0;
  if (!toque && !reduz) {
    window.addEventListener("mousemove", function (e) {
      alvoX = (e.clientX / window.innerWidth - 0.5);
      alvoY = (e.clientY / window.innerHeight - 0.5);
    }, { passive: true });
  }

  var header = $(".site-header");
  var ultimoY = -1;

  function loop() {
    var y = window.scrollY || window.pageYOffset;
    var vh = window.innerHeight;
    mouseX += (alvoX - mouseX) * 0.08;
    mouseY += (alvoY - mouseY) * 0.08;

    if (y !== ultimoY) {
      header.style.setProperty("--header-a", Math.min(0.92, 0.35 + y / 400).toFixed(3));
      ultimoY = y;
    }

    for (var i = 0; i < camadas.length; i++) {
      var c = camadas[i];
      var r = c.el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) continue;
      var centro = (r.top + r.height / 2 - vh / 2);
      var ty = -centro * c.d * 0.25;
      var mx = toque ? 0 : mouseX * c.d * 24;
      var my = toque ? 0 : mouseY * c.d * 16;
      c.el.style.transform = "translate3d(" + mx.toFixed(1) + "px," + (ty + my).toFixed(1) + "px,0)";
    }

    if (pending.length) {
      var resta = [];
      for (var j = 0; j < pending.length; j++) {
        var el = pending[j];
        var t = el.getBoundingClientRect().top;
        if (t < vh * 0.9) el.classList.add("visto"); else resta.push(el);
      }
      pending = resta;
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  /* ---------- lightcard + cursor ring (desktop) ---------- */
  function ligaLightcard(el) {
    if (toque || el.__lc) return;
    el.__lc = true;
    el.addEventListener("mousemove", function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (e.clientX - r.left) + "px");
      el.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  }
  $$(".lightcard").forEach(ligaLightcard);

  if (!toque && !reduz) {
    var ring = document.createElement("div");
    ring.className = "cursor-ring";
    ring.setAttribute("aria-hidden", "true");
    document.body.appendChild(ring);
    var rx = 0, ry = 0, cx = 0, cy = 0;
    window.addEventListener("mousemove", function (e) {
      cx = e.clientX; cy = e.clientY; ring.classList.add("ativo");
      var alvo = e.target.closest && e.target.closest("a, button, input, select, textarea");
      ring.classList.toggle("grande", !!alvo);
    }, { passive: true });
    (function anel() {
      rx += (cx - rx) * 0.2; ry += (cy - ry) * 0.2;
      ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
      requestAnimationFrame(anel);
    })();
  }

  /* ---------- menu mobile ---------- */
  var toggle = $(".menu-toggle");
  function fechaMenu() { doc.classList.remove("nav-aberto"); if (toggle) toggle.setAttribute("aria-expanded", "false"); }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var aberto = doc.classList.toggle("nav-aberto");
      toggle.setAttribute("aria-expanded", aberto ? "true" : "false");
    });
    $$(".main-nav a").forEach(function (a) { a.addEventListener("click", fechaMenu); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") fechaMenu(); });
  }

  /* ---------- portfólio: filtro ---------- */
  var itens = $$(".pf-item");
  var visiveis = itens.slice();
  $$(".filtro").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filtro");
      $$(".filtro").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      visiveis = [];
      itens.forEach(function (it) {
        var mostra = f === "todos" || it.getAttribute("data-cat") === f;
        it.hidden = !mostra;
        if (mostra) visiveis.push(it);
      });
      indice = 0;
    });
  });

  /* ---------- lightbox ---------- */
  var lb = $(".lightbox"), lbImg = $(".lightbox img"), lbTit = $(".lb-tit"), lbLeg = $(".lb-leg"), lbPos = $(".lb-pos");
  var indice = 0, focoAnterior = null;
  function mostra(i) {
    if (!visiveis.length) return;
    indice = (i + visiveis.length) % visiveis.length;
    var it = visiveis[indice];
    lbImg.src = it.getAttribute("href");
    lbImg.alt = it.querySelector("img").alt;
    lbTit.textContent = it.getAttribute("data-titulo");
    lbLeg.textContent = it.getAttribute("data-legenda");
    lbPos.textContent = (indice + 1) + " / " + visiveis.length;
  }
  function abre(i) {
    focoAnterior = document.activeElement;
    lb.classList.add("aberto"); lb.setAttribute("aria-hidden", "false");
    doc.style.overflow = "hidden";
    mostra(i);
    $(".lb-fechar").focus();
  }
  function fecha() {
    lb.classList.remove("aberto"); lb.setAttribute("aria-hidden", "true");
    doc.style.overflow = "";
    if (focoAnterior) focoAnterior.focus();
  }
  itens.forEach(function (it) {
    it.addEventListener("click", function (e) {
      e.preventDefault();
      abre(visiveis.indexOf(it));
    });
  });
  if (lb) {
    $(".lightbox-backdrop").addEventListener("click", fecha);
    $(".lb-fechar").addEventListener("click", fecha);
    $(".lb-ant").addEventListener("click", function () { mostra(indice - 1); });
    $(".lb-prox").addEventListener("click", function () { mostra(indice + 1); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("aberto")) return;
      if (e.key === "Escape") $(".lb-fechar").click();
      else if (e.key === "ArrowLeft") $(".lb-ant").click();
      else if (e.key === "ArrowRight") $(".lb-prox").click();
      else if (e.key === "Tab") { /* focus trap */
        var f = $$(".lb-btn", lb), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
    var toqueX = null;
    lb.addEventListener("touchstart", function (e) { toqueX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (toqueX === null) return;
      var dx = e.changedTouches[0].clientX - toqueX;
      if (Math.abs(dx) > 50) mostra(indice + (dx < 0 ? 1 : -1));
      toqueX = null;
    });
  }

  /* ---------- serviço pré-selecionado a partir dos cards ---------- */
  var select = $("#servico");
  $$("[data-servico]").forEach(function (a) {
    a.addEventListener("click", function () { if (select) select.value = a.getAttribute("data-servico"); });
  });

  /* ---------- formulário -> WhatsApp ---------- */
  function utm() {
    try { return JSON.parse(sessionStorage.getItem("sf_utm") || "{}"); } catch (e) { return window.__SF_UTM || {}; }
  }
  var form = $("#form-orcamento");
  if (form) {
    var erro = $(".form-erro", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = {
        nome: form.nome.value.trim(),
        telefone: form.telefone.value.trim(),
        servico: form.servico.options[form.servico.selectedIndex].text,
        mensagem: form.mensagem.value.trim()
      };
      if (!d.nome || d.telefone.replace(/\D/g, "").length < 10 || !form.servico.value) {
        erro.textContent = "Preencha nome, telefone com DDD e o serviço.";
        return;
      }
      erro.textContent = "";
      var linhas = [
        "Olá! Vim pelo site e quero um orçamento.",
        "*Nome:* " + d.nome,
        "*Telefone:* " + d.telefone,
        "*Serviço:* " + d.servico
      ];
      if (d.mensagem) linhas.push("*Detalhes:* " + d.mensagem);
      var u = utm();
      if (u.utm_source) linhas.push("_(origem: " + [u.utm_source, u.utm_medium, u.utm_campaign].filter(Boolean).join(" / ") + ")_");
      var url = "https://wa.me/" + CFG.whatsapp + "?text=" + encodeURIComponent(linhas.join("\n"));
      if (typeof window.rastrearConversao === "function") window.rastrearConversao(d.servico);
      window.location.href = url;
    });
  }

  /* ---------- clique em qualquer botão de WhatsApp também conta como contato ---------- */
  $$("a[href^='https://wa.me/']").forEach(function (a) {
    a.addEventListener("click", function () {
      if (typeof window.rastrearContato === "function") window.rastrearContato();
    });
  });
})();
