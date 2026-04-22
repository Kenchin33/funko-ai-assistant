from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["Widget"])


@router.get("/widget.js")
def get_widget_script():
    js = """
(function () {
  if (window.FunkoAssistantWidgetLoaded) return;
  window.FunkoAssistantWidgetLoaded = true;

  const ASSISTANT_IFRAME_URL = "http://localhost:5174/widget";

  const launcher = document.createElement("button");
  launcher.setAttribute("type", "button");
  launcher.setAttribute("aria-label", "Open assistant");
  launcher.innerHTML = "💬";

  Object.assign(launcher.style, {
    position: "fixed",
    right: "20px",
    bottom: "20px",
    width: "68px",
    height: "68px",
    border: "none",
    borderRadius: "999px",
    background: "#2b2b2b",
    color: "#ffffff",
    fontSize: "28px",
    cursor: "pointer",
    zIndex: "999999",
    boxShadow: "0 12px 30px rgba(0,0,0,0.18)"
  });

  const container = document.createElement("div");
  Object.assign(container.style, {
    position: "fixed",
    right: "20px",
    bottom: "100px",
    width: "380px",
    height: "640px",
    background: "#ffffff",
    borderRadius: "24px",
    overflow: "hidden",
    zIndex: "999998",
    boxShadow: "0 18px 45px rgba(0,0,0,0.18)",
    display: "none"
  });

  const iframe = document.createElement("iframe");
  iframe.src = ASSISTANT_IFRAME_URL;
  iframe.title = "Funko AI Assistant";
  iframe.setAttribute("allow", "clipboard-write");
  Object.assign(iframe.style, {
    width: "100%",
    height: "100%",
    border: "none",
    display: "block",
    background: "#fff"
  });

  container.appendChild(iframe);

  launcher.addEventListener("click", function () {
    const isOpen = container.style.display === "block";
    container.style.display = isOpen ? "none" : "block";
    launcher.innerHTML = isOpen ? "💬" : "×";
  });

  function handleResize() {
    if (window.innerWidth <= 640) {
      container.style.left = "12px";
      container.style.right = "12px";
      container.style.width = "auto";
      container.style.height = "70vh";
      container.style.bottom = "90px";

      launcher.style.right = "16px";
      launcher.style.bottom = "16px";
    } else {
      container.style.left = "";
      container.style.right = "20px";
      container.style.width = "380px";
      container.style.height = "640px";
      container.style.bottom = "100px";

      launcher.style.right = "20px";
      launcher.style.bottom = "20px";
    }
  }

  window.addEventListener("resize", handleResize);
  handleResize();

  document.body.appendChild(container);
  document.body.appendChild(launcher);
})();
"""
    return Response(content=js, media_type="application/javascript")