
// Variables

let image = document.querySelector('.img').src;
let url = "url('" + image + "')";
let bkg = document.querySelector('.section');

// Dynamic Background

bkg.style.background = 'linear-gradient(rgba(0, 0, 0, 0.486), rgba(0, 0, 0, 0.801))'+' ,' + url;
bkg.style.backgroundPosition = 'center';
bkg.style.backgroundRepeat = 'no-repeat';
bkg.style.backgroundSize = 'cover';