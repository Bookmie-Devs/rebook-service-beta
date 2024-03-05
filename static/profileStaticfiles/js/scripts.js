
// Variables

let images = document.querySelectorAll('.img');

images.forEach(img => {
 if(img.parentElement.classList.contains('active')){
let url = "url('" + img.src + "')";
let bkg = document.querySelector('.section');

// Dynamic Background

bkg.style.background = 'linear-gradient(rgba(0, 0, 0, 0.486), rgba(0, 0, 0, 0.801))'+' ,' + url;
bkg.style.backgroundPosition = 'center';
bkg.style.backgroundRepeat = 'no-repeat';
bkg.style.backgroundSize = 'cover';
 }
});

let currentIndex = 0;  // Initialize with the first image

function checkBgf() {
  images.forEach((img, index) => {
    if (img.parentElement.classList.contains('active')) {
      currentIndex = index;  // Update the current index
      let nextIndex = (currentIndex + 1) % images.length;  // Calculate the next index

      let url = "url('" + images[nextIndex].src + "')";
      let bkg = document.querySelector('.section');

      // Dynamic Background
      bkg.style.background = 'linear-gradient(rgba(0, 0, 0, 0.486), rgba(0, 0, 0, 0.801))' + ',' + url;
      bkg.style.backgroundPosition = 'center';
      bkg.style.backgroundRepeat = 'no-repeat';
      bkg.style.backgroundSize = 'cover';
    }
  });
}

function checkBgb() {
  images.forEach((img, index) => {
    if (img.parentElement.classList.contains('active')) {
      currentIndex = index;  // Update the current index
      let prevIndex = (currentIndex - 1) % images.length;  // Calculate the prev index

      let url = "url('" + images[prevIndex].src + "')";
      let bkg = document.querySelector('.section');

      // Dynamic Background
      bkg.style.background = 'linear-gradient(rgba(0, 0, 0, 0.486), rgba(0, 0, 0, 0.801))' + ',' + url;
      bkg.style.backgroundPosition = 'center';
      bkg.style.backgroundRepeat = 'no-repeat';
      bkg.style.backgroundSize = 'cover';
    }
  });
}


function openNav() {
    document.getElementById("menu-btn").classList.toggle("menu_btn-style")
}
