// custom.js

// Example: Highlight a table row when clicked
document.querySelectorAll('.table tbody tr').forEach(row => {
    row.addEventListener('click', () => {
        row.classList.toggle('bg-info');
    });
});
