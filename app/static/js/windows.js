 // профиль
 function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
  }
  
  function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
  }
  
  function showPage(pageId) {
    const profileSection = document.querySelector('.profile-section');
    if (profileSection) profileSection.style.display = 'none';
    
    const pages = document.querySelectorAll('.page-content-p2');
    pages.forEach(page => {
      page.classList.remove('active');
    });
    
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
      selectedPage.classList.add('active');
    }
  }
  
  function showProfilePage() {
    const pages = document.querySelectorAll('.page-content-p2');
    pages.forEach(page => {
      page.classList.remove('active');
    });
  
    const profileSection = document.querySelector('.profile-section');
    if (profileSection) {
      profileSection.style.display = 'flex'; 
      profileSection.style.justifyContent = 'center'; 
      profileSection.style.alignItems = 'center';  
    }
}
  
  function saveProfile() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const fullName = document.getElementById('fullName').value;
    const phone = document.getElementById('phone').value;
    
    alert('Profile updated successfully!');
    closeModal('editProfileModal');
  }
  
  function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (newPassword !== confirmPassword) {
      alert('New passwords do not match!');
      return;
    }
    
    alert('Password updated successfully!');
    closeModal('changePasswordModal');
  }
  
  // избранное
  function removeFavorite(element) {
    const favoriteItem = element.closest('.favorite-item-p2');
    favoriteItem.style.opacity = '0';
    setTimeout(() => {
      favoriteItem.remove();
    }, 300);
  }

  document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.querySelector('.profile-actions button:nth-child(1)');
    const changePasswordBtn = document.querySelector('.profile-actions button:nth-child(2)');
    const orderHistoryLink = document.getElementById('orderHistoryLink');
    const favoritesLink = document.getElementById('favoritesLink');
    const addressesLink = document.getElementById('addressesLink');
    
    if (editProfileBtn) {
      editProfileBtn.addEventListener('click', function() {
        openModal('editProfileModal');
      });
    }
    
    if (changePasswordBtn) {
      changePasswordBtn.addEventListener('click', function() {
        openModal('changePasswordModal');
      });
    }
    
    if (orderHistoryLink) {
      orderHistoryLink.addEventListener('click', function(e) {
        e.preventDefault();
        showPage('orderHistoryPage');
      });
    }
    
    if (favoritesLink) {
      favoritesLink.addEventListener('click', function(e) {
        e.preventDefault();
        showPage('favoritesPage');
      });
    }
    
    if (addressesLink) {
      addressesLink.addEventListener('click', function(e) {
        e.preventDefault();
        showPage('addressesPage');
      });
    }
  });