/* ==========================================================================
   FirstStep.ai Designer - Frontend Interactivity Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Modal Controls
    const createModal = document.getElementById('createProjectModal');
    const openModalBtn = document.getElementById('openCreateModal');
    const openModalShortcut = document.getElementById('openCreateModalShortcut');
    const closeModalBtn = document.getElementById('closeCreateModal');
    const cancelModalBtn = document.getElementById('cancelCreateModal');
    const createForm = document.getElementById('createProjectForm');
    
    const toggleModal = (isOpen) => {
        if (createModal) {
            if (isOpen) {
                createModal.classList.add('open');
                // Focus on name input
                setTimeout(() => {
                    const nameInput = document.getElementById('projectNameInput');
                    if (nameInput) nameInput.focus();
                }, 100);
            } else {
                createModal.classList.remove('open');
                if (createForm) createForm.reset();
            }
        }
    };

    if (openModalBtn) openModalBtn.addEventListener('click', () => toggleModal(true));
    if (openModalShortcut) openModalShortcut.addEventListener('click', (e) => {
        e.preventDefault();
        toggleModal(true);
    });
    if (closeModalBtn) closeModalBtn.addEventListener('click', () => toggleModal(false));
    if (cancelModalBtn) cancelModalBtn.addEventListener('click', () => toggleModal(false));
    
    // Close modal on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && createModal && createModal.classList.contains('open')) {
            toggleModal(false);
        }
    });

    // Close modal if clicking overlay backdrop
    if (createModal) {
        createModal.addEventListener('click', (e) => {
            if (e.target === createModal) {
                toggleModal(false);
            }
        });
    }

    // 2. Auto-Save Tag Select Changes Asynchronously
    const tagSelectors = document.querySelectorAll('.tag-select');
    tagSelectors.forEach(select => {
        select.addEventListener('change', async (e) => {
            const projectId = select.getAttribute('data-project-id');
            const newTag = select.value;
            
            // Show loading style or indicator
            select.style.opacity = '0.6';
            
            try {
                const response = await fetch(`/api/projects/${projectId}/tag`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ tag: newTag })
                });
                
                const result = await response.json();
                select.style.opacity = '1';
                
                if (response.ok && result.success) {
                    showToast(`Tag saved to "${newTag}"!`, 'success');
                } else {
                    showToast(result.detail || 'Failed to save tag', 'error');
                }
            } catch (err) {
                select.style.opacity = '1';
                showToast('Network error while saving tag', 'error');
                console.error(err);
            }
        });
    });

    // 3. Clone Project Mock Animation & Alert
    const cloneButtons = document.querySelectorAll('.btn-clone');
    cloneButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const projectName = btn.getAttribute('data-project-name');
            showToast(`Cloning dataset for "${projectName}"...`, 'info');
            
            // Mock delay and reload
            setTimeout(() => {
                showToast(`Project "${projectName}" cloned successfully!`, 'success');
                // Optional: We can trigger a form submission to create a clone on the backend
                // but a visual mock alert in this demonstration version is exceptionally clean.
            }, 1200);
        });
    });

    // 4. Toast Notification Engine
    const showToast = (message, type = 'success') => {
        // Create container if not exists
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        // Create toast
        const toast = document.createElement('div');
        toast.className = `toast ${type === 'error' ? 'toast-error' : ''}`;
        
        // Icon pick based on type
        let iconName = 'check-circle';
        if (type === 'error') iconName = 'alert-triangle';
        else if (type === 'info') iconName = 'info';
        
        toast.innerHTML = `
            <i data-lucide="${iconName}" style="width: 16px; height: 16px;"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        lucide.createIcons(); // Initialize the new icon
        
        // Remove toast after delay
        setTimeout(() => {
            toast.style.animation = 'slide-up-toast 0.3s ease reverse forwards';
            setTimeout(() => {
                toast.remove();
                if (container.children.length === 0) {
                    container.remove();
                }
            }, 300);
        }, 3000);
    };

    // 5. Handle URL Search Param Errors/Notifications
    const urlParams = new URLSearchParams(window.location.search);
    const errorMsg = urlParams.get('error');
    if (errorMsg) {
        showToast(decodeURIComponent(errorMsg), 'error');
        // Clean the URL without reloading
        const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + (urlParams.get('status') ? '?status=' + urlParams.get('status') : '');
        window.history.replaceState({ path: cleanUrl }, '', cleanUrl);
    }
    
    // Help floating support click
    const helpBtn = document.querySelector('.floating-help-btn');
    if (helpBtn) {
        helpBtn.addEventListener('click', () => {
            showToast('Help assistant is ready! How can we assist you?', 'info');
        });
    }
});
