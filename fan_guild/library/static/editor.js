// Данный скрипт предназначен для редактора глав произведений в формате markdown
const chapterTitle = document.getElementById("chapterTitle");
const toast = document.getElementById("toast");

const editor = document.getElementById("editor");
const preview = document.getElementById("preview");

const previewTitle = document.getElementById("previewTitle");

const layoutMode = document.getElementById("layoutMode");
const themeSelect = document.getElementById("themeSelect");
const editorFont = document.getElementById("editorFont");
const previewFont = document.getElementById("previewFont");
const fontSize = document.getElementById("fontSize");
const fontSizeValue = document.getElementById("fontSizeValue");

const hoverZone = document.querySelector(".top-hover-zone");
const toolbar = document.getElementById("toolbar");
const saveChapterBtn = document.getElementById("saveChapterBtn");
const exportMarkdownBtn = document.getElementById("exportMarkdownBtn");
const singleModeGroup = document.getElementById("singleModeGroup");
const modeButtons = document.querySelectorAll(".mode-btn");
const focusSink = document.getElementById("focusSink");
const STORAGE_KEYS = {
    content: "novel_editor_content",
    layout: "novel_editor_layout",
    singleView: "novel_editor_single_view",
    theme: "novel_editor_theme",
    editorFont: "novel_editor_editor_font",
    previewFont: "novel_editor_preview_font",
    fontSize: "novel_editor_font_size"
};

const FONT_OPTIONS = [
    "По умолчанию",
    "Times New Roman",
    "Georgia",
    "Arial",
    "Garamond"
];

function clearEditorFocus() {
    if (editor) {
        editor.blur();
    }

    if (document.activeElement && typeof document.activeElement.blur === "function") {
        document.activeElement.blur();
    }

    if (focusSink) {
        focusSink.focus({ preventScroll: true });
    }
}

function populateFontSelect(selectElement, fonts, selectedValue) {
    if (!selectElement) return;

    selectElement.innerHTML = "";

    fonts.forEach((fontName) => {
        const option = document.createElement("option");
        option.value = fontName;
        option.textContent = fontName;
        selectElement.appendChild(option);
    });

    if (selectedValue && fonts.includes(selectedValue)) {
        selectElement.value = selectedValue;
    } else {
        selectElement.value = "По умолчанию";
    }
}

function initFontSelects() {
    const savedEditorFont =
        localStorage.getItem(STORAGE_KEYS.editorFont) || "По умолчанию";
    const savedPreviewFont =
        localStorage.getItem(STORAGE_KEYS.previewFont) || "По умолчанию";

    populateFontSelect(editorFont, FONT_OPTIONS, savedEditorFont);
    populateFontSelect(previewFont, FONT_OPTIONS, savedPreviewFont);
}

function getFontStack(fontName, kind = "preview") {
    const serifDefault = '"Times New Roman", Georgia, serif';
    const monoDefault = 'Consolas, "Courier New", monospace';

    if (!fontName || fontName === "По умолчанию") {
        return kind === "editor" ? monoDefault : serifDefault;
    }

    switch (fontName) {
        case "Times New Roman":
            return '"Times New Roman", Georgia, serif';

        case "Georgia":
            return 'Georgia, "Times New Roman", serif';

        case "Arial":
            return 'Arial, Helvetica, sans-serif';

        case "Helvetica":
            return 'Helvetica, Arial, sans-serif';

        case "Garamond":
            return 'Garamond, "Times New Roman", Georgia, serif';

        default:
            return kind === "editor" ? monoDefault : serifDefault;
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderMarkdown() {
    if (!editor || !preview || typeof marked === "undefined") return;

    syncPreviewTitle();
    preview.innerHTML = marked.parse(editor.value);
}

function saveContentToStorage() {
    if (!editor) return;
    localStorage.setItem(getContentStorageKey(), editor.value);
}

function loadContentFromStorage() {
    if (!editor) return;

    const saved = localStorage.getItem(getContentStorageKey());

    if (saved !== null) {
        editor.value = saved;
    }
}

function applyLayout(mode) {
    document.body.classList.remove("split-mode", "single-mode");
    document.body.classList.add(mode === "single" ? "single-mode" : "split-mode");

    if (mode === "single") {
        const savedView =
            localStorage.getItem(STORAGE_KEYS.singleView) || "editor";

        document.body.classList.remove("view-editor", "view-preview");
        document.body.classList.add(
            savedView === "preview" ? "view-preview" : "view-editor"
        );
    } else {
        document.body.classList.remove("view-editor", "view-preview");
        if (editor) {
            editor.blur();
        }
    }

    if (layoutMode) {
        layoutMode.value = mode;
    }

    localStorage.setItem(STORAGE_KEYS.layout, mode);
    updateSingleModeControls();
    moveFocusForCurrentView();
}

function applySingleView(view) {
    if (!document.body.classList.contains("single-mode")) return;

    document.body.classList.remove("view-editor", "view-preview");
    document.body.classList.add(view === "preview" ? "view-preview" : "view-editor");

    localStorage.setItem(STORAGE_KEYS.singleView, view);
    updateSingleModeControls();
    moveFocusForCurrentView();
}

function updateSingleModeControls() {
    const isSingle = document.body.classList.contains("single-mode");

    if (singleModeGroup) {
        singleModeGroup.style.opacity = isSingle ? "1" : "0.45";
    }

    modeButtons.forEach((btn) => {
        const shouldBeActive =
            isSingle && document.body.classList.contains(`view-${btn.dataset.view}`);

        btn.disabled = !isSingle;
        btn.classList.toggle("active", shouldBeActive);
    });
}

function applyTheme(theme) {
    document.body.classList.remove(
        "theme-dark",
        "theme-light",
        "theme-sepia",
        "theme-graphite"
    );
    document.body.classList.add(`theme-${theme}`);

    if (themeSelect) {
        themeSelect.value = theme;
    }

    localStorage.setItem(STORAGE_KEYS.theme, theme);
}

function applyEditorFont(fontName) {
    const fontStack = getFontStack(fontName, "editor");

    document.documentElement.style.setProperty("--editor-font", fontStack);

    if (editorFont) {
        editorFont.value = fontName;
    }

    localStorage.setItem(STORAGE_KEYS.editorFont, fontName);
}

function applyPreviewFont(fontName) {
    const fontStack = getFontStack(fontName, "preview");

    document.documentElement.style.setProperty("--preview-font", fontStack);

    if (previewFont) {
        previewFont.value = fontName;
    }

    localStorage.setItem(STORAGE_KEYS.previewFont, fontName);
}

function applyFontSize(size) {
    const safeSize = String(size);
    document.documentElement.style.setProperty("--font-size", `${safeSize}px`);

    if (fontSize) {
        fontSize.value = safeSize;
    }

    if (fontSizeValue) {
        fontSizeValue.textContent = `${safeSize}px`;
    }

    localStorage.setItem(STORAGE_KEYS.fontSize, safeSize);
}

async function exportMarkdownToFile() {
    if (!editor) return;

    const content = editor.value;
    const defaultFileName = "chapter.md";

    if ("showSaveFilePicker" in window) {
        try {
            const handle = await window.showSaveFilePicker({
                suggestedName: defaultFileName,
                types: [
                    {
                        description: "Markdown files",
                        accept: {
                            "text/markdown": [".md"],
                            "text/plain": [".txt"]
                        }
                    }
                ]
            });

            const writable = await handle.createWritable();
            await writable.write(content);
            await writable.close();
            return;
        } catch (error) {
            if (error && error.name === "AbortError") {
                return;
            }
        }
    }

    const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = defaultFileName;
    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

let hideToolbarTimer = null;

function showToolbar() {
    clearTimeout(hideToolbarTimer);
    document.body.classList.add("toolbar-visible");
}

function hideToolbarDelayed() {
    clearTimeout(hideToolbarTimer);
    hideToolbarTimer = setTimeout(() => {
        document.body.classList.remove("toolbar-visible");
    }, 180);
}

function initToolbarHover() {
    if (hoverZone) {
        hoverZone.addEventListener("mouseenter", showToolbar);
    }

    if (toolbar) {
        toolbar.addEventListener("mouseenter", showToolbar);
        toolbar.addEventListener("mouseleave", hideToolbarDelayed);
    }
}

function initControls() {
    if (layoutMode) {
        layoutMode.addEventListener("change", () => {
            applyLayout(layoutMode.value);
        });
    }

    modeButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            applySingleView(btn.dataset.view);
        });
    });

    if (themeSelect) {
        themeSelect.addEventListener("change", () => {
            applyTheme(themeSelect.value);
        });
    }

    if (editorFont) {
        editorFont.addEventListener("change", () => {
            applyEditorFont(editorFont.value);
        });
    }

    if (previewFont) {
        previewFont.addEventListener("change", () => {
            applyPreviewFont(previewFont.value);
        });
    }

    if (saveChapterBtn) {
        saveChapterBtn.addEventListener("click", async () => {
            const defaultText = "Сохранить главу";

            try {
                saveChapterBtn.disabled = true;
                saveChapterBtn.textContent = "Сохранение...";

                const result = await saveChapterToBackend();
                console.log("Глава сохранена:", result);

                saveChapterBtn.textContent = "Сохранено";
                showToast("Глава успешно сохранена", "success");

                setTimeout(() => {
                    saveChapterBtn.textContent = defaultText;
                    saveChapterBtn.disabled = false;
                }, 1200);
            } catch (error) {
                console.error(error);
                showToast(error.message || "Не удалось сохранить главу", "error");
                saveChapterBtn.textContent = defaultText;
                saveChapterBtn.disabled = false;
            }
        });
    }

    if (fontSize) {
        fontSize.addEventListener("input", () => {
            applyFontSize(fontSize.value);
        });
    }

    if (exportMarkdownBtn) {
        exportMarkdownBtn.addEventListener("click", async () => {
            await exportMarkdownToFile();
        });
    }
}

function moveFocusForCurrentView() {
    requestAnimationFrame(() => {
        const isSingle = document.body.classList.contains("single-mode");
        const isPreview = document.body.classList.contains("view-preview");

        if (isSingle && isPreview) {
            clearEditorFocus();
            if (preview) {
                preview.focus({ preventScroll: true });
            }
        } else {
            if (preview && document.activeElement === preview) {
                preview.blur();
            }
        }
    });
}

document.addEventListener("mousedown", (event) => {
    const clickedInsideEditor = editor && editor.contains(event.target);
    const clickedInsidePreview = preview && preview.contains(event.target);
    const clickedInsideToolbar = toolbar && toolbar.contains(event.target);
    const clickedModeButton = event.target.closest(".mode-btn");

    if (
        clickedInsideEditor ||
        clickedInsidePreview ||
        clickedInsideToolbar ||
        clickedModeButton
    ) {
        return;
    }

    clearEditorFocus();
});

document.addEventListener("input", (event) => {
    if (event.target && event.target.id === "chapterTitle") {
        syncPreviewTitle();
    }
});

function syncPreviewTitle() {
    const currentTitleInput = document.getElementById("chapterTitle");
    const currentPreviewTitle = document.getElementById("previewTitle");

    if (!currentTitleInput || !currentPreviewTitle) return;

    currentPreviewTitle.textContent = currentTitleInput.value.trim() || "Без названия";
}

function initEditor() {
    if (!editor) return;

    loadContentFromStorage();
    renderMarkdown();

    editor.addEventListener("input", () => {
        renderMarkdown();
        saveContentToStorage();
    });

    syncPreviewTitle();
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split("; ") : [];

    for (const cookie of cookies) {
        const parts = cookie.split("=");
        const key = parts[0];
        const value = parts.slice(1).join("=");

        if (key === name) {
            return decodeURIComponent(value);
        }
    }

    return null;
}

async function saveChapterToBackend() {
    const saveUrl = saveChapterBtn?.dataset.saveUrl;
    const csrfToken = getCookie("csrftoken");

    if (!saveUrl) {
        throw new Error("Не найден URL сохранения.");
    }
    console.log("SAVE URL =", saveUrl);
    const response = await fetch(saveUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            title: chapterTitle ? chapterTitle.value.trim() : "",
            content: editor ? editor.value : ""
        })
    });

    const contentType = response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
        const text = await response.text();
        console.error("Сервер вернул не JSON:", text);
        throw new Error("Сервер вернул HTML вместо JSON. Проверь save_url и Django view.");
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Ошибка сохранения");
    }

    return data;
}

function initFromStorage() {
    const savedLayout = localStorage.getItem(STORAGE_KEYS.layout) || "split";
    const savedTheme = localStorage.getItem(STORAGE_KEYS.theme) || "dark";
    const savedEditorFont =
        localStorage.getItem(STORAGE_KEYS.editorFont) || "По умолчанию";
    const savedPreviewFont =
        localStorage.getItem(STORAGE_KEYS.previewFont) || "По умолчанию";
    const savedFontSize = localStorage.getItem(STORAGE_KEYS.fontSize) || "18";

    applyTheme(savedTheme);
    applyEditorFont(savedEditorFont);
    applyPreviewFont(savedPreviewFont);
    applyFontSize(savedFontSize);
    applyLayout(savedLayout);
}

let toastTimer = null;

function getContentStorageKey() {
    const chapterId = document.body.dataset.chapterId;

    if (!chapterId) {
        throw new Error("Не найден data-chapter-id на <body>");
    }

    return `${STORAGE_KEYS.content}_${chapterId}`;
}

function initTitleSync() {
    if (!chapterTitle) return;

    const updatePreviewTitle = () => {
        syncPreviewTitle();
    };

    chapterTitle.addEventListener("input", updatePreviewTitle);
    chapterTitle.addEventListener("change", updatePreviewTitle);

    requestAnimationFrame(updatePreviewTitle);
}

function showToast(message, type = "success") {
    if (!toast) return;

    toast.textContent = message;
    toast.classList.remove("success", "error", "show");
    toast.classList.add(type);

    // форсируем перерисовку, чтобы анимация стабильно срабатывала
    void toast.offsetWidth;

    toast.classList.add("show");

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.classList.remove("show");
    }, 2200);
}

function init() {
    initFontSelects();
    initToolbarHover();
    initControls();
    initTitleSync();
    initEditor();
    initFromStorage();
    updateSingleModeControls();
    moveFocusForCurrentView();
}

init();