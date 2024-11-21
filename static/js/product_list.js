    // Lógica para cambiar entre vistas de lista y cuadrícula
    const listViewBtn = document.getElementById('list-view-btn');
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listView = document.getElementById('list-view');
    const gridView = document.getElementById('grid-view');

    listViewBtn.addEventListener('click', () => {
        listView.style.display = 'block';
        gridView.style.display = 'none';
    });

    gridViewBtn.addEventListener('click', () => {
        gridView.style.display = 'grid';
        listView.style.display = 'none';
    });

    // Establecer vista predeterminada
    listView.style.display = 'block';
    gridView.style.display = 'none';
