import { basic, initSidebar, initTopbar } from './modules/layouts';
import { loadImg, imgPopup, initClipboard } from './modules/plugins';

loadImg();
imgPopup();
initSidebar();
initTopbar();
initClipboard();
basic();
cardClick();

function cardClick(event, url) {
    // Prevent navigation if an <a> tag or a descendant is clicked
        if (event.target.tagName.toLowerCase() !== 'a' && !event.target.closest('a')) {
            window.location.href = url;
        }
    }