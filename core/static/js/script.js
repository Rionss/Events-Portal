function openNav() {
  const header = document.querySelector('.header');
  if (header.style.gridTemplateRows == "60px auto") {
    header.style.gridTemplateRows = "60px 0";
  } else {
    header.style.gridTemplateRows = "60px auto";
  }
}

function dropDown() {
  const dropdown = document.querySelector('.dropdown');
  if (dropdown.style.display == "flex") {
    dropdown.style.display = "none"
  } else {
    dropdown.style.display = "flex"
  }
}

window.onclick = function(event) {
  if (!event.target.matches('.auth-thumbnail')) {
    var dropdowns = document.getElementsByClassName("dropdown");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.style.display=='flex') {
        openDropdown.style.display='none';
      }
    }
  }
}