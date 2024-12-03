

document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
        location.reload(); 
    }
});

window.addEventListener("pageshow", (event) => {
    if (event.persisted) { 
        location.reload(); 
    }
});