/*!
 * @license Copyright (c) 2003-2022, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md.
 */
(() => {
    "use strict";
    const e = {
        tokenUrl: "https://33333.cke-cs.com/token/dev/ijrDsqFix838Gh3wGO3F77FSW94BwcLXprJ4APSp3XQ26xsUHTi0jcb1hoBt",
        uploadUrl: "https://33333.cke-cs.com/easyimage/upload/"
    };
    ClassicEditor.create(document.querySelector("#snippet-read-only-toolbar"), {
        cloudServices: e,
        ui: {
            viewportOffset: {
                top: window.getViewportTopOffsetConfig()
            }
        }
    }).then((e => {
        window.editor = e;
        const t = document.querySelector("#snippet-read-only-toggle-toolbar");
        t.addEventListener("click", (() => {
            e.isReadOnly = !e.isReadOnly, t.innerText = e.isReadOnly ? "Composer" : "Annuler"
        }));
        const o = e.ui.view.toolbar.element;
        e.on("change:isReadOnly", ((e, t, i) => {
            o.style.display = i ? "none" : "flex"
        }))
    })).catch((e => {
        console.error(e.stack)
    }))
})();