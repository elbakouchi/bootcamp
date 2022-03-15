/*!
 * @license Copyright (c) 2003-2022, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md.
 */
(() => {
    "use strict";
    const d = {
        tokenUrl: "https://33333.cke-cs.com/token/dev/ijrDsqFix838Gh3wGO3F77FSW94BwcLXprJ4APSp3XQ26xsUHTi0jcb1hoBt",
        uploadUrl: "https://33333.cke-cs.com/easyimage/upload/"
    };
    ClassicEditor.create(document.querySelector("#snippet-read-only-toolbar"), {
        cloudServices: d,
        ui: {
            viewportOffset: {
                top: window.getViewportTopOffsetConfig()
            }
        }
    }).then((e => {
        window.editor = e;
        const o = e.ui.view.toolbar.element;
        o.style.display = "none";
        e.on("change:isReadOnly", ((e, t, i) => {
            console.log(i);
            o.style.display = !i ? "none" : "flex"
        }))
        const t = document.querySelector("#snippet-read-only-toggle-toolbar");
        t.addEventListener("click", (() => {
            e.isReadOnly = e.isReadOnly, t.innerText = e.isReadOnly ? "Annuler" : "Composer"
        }));
    })).catch((e => {
        console.error(e.stack)
    }))
})();