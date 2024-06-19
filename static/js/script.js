function calculerPuissance() {
    const Pt = document.getElementById('Pt').value;
    const d = document.getElementById('d').value;
    const f = document.getElementById('f').value;
    const Le = document.getElementById('Le').value;
    const Gt = document.getElementById('Gt').value;
    const Gr = document.getElementById('Gr').value;

    const data = {
        Pt: parseFloat(Pt),
        d: parseFloat(d),
        f: parseFloat(f),
        Le: parseFloat(Le),
        Gt: parseFloat(Gt),
        Gr: parseFloat(Gr)
    };

    fetch('/calculer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultatDiv = document.getElementById('resultat');
        resultatDiv.innerHTML = `Puissance reçue: ${data.Pr.toFixed(2)} dBm`;
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}
