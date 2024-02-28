const flyingTexts = [];

function flyText() {
    if (flyingTexts.length >= 15) {
        alert('더 이상 추가할 수 없습니다.');
        return;
    }

    const text = document.getElementById('inputText').value;
    if (text !== '') {
        const flyingText = document.createElement('div');
        flyingText.textContent = text;
        flyingText.style.position = 'absolute';
        flyingText.style.left = `${Math.random() * 90}%`;
        flyingText.style.top = `${Math.random() * 40}vh`;
        flyingText.style.color = `#${Math.floor(Math.random()*16777215).toString(16)}`;
        flyingText.style.fontSize = `${Math.random() * 2 + 1}em`;
        flyingText.style.whiteSpace = 'nowrap';

        const direction = Math.random() < 0.5 ? -1 : 1;
        const speed = Math.random() * 2 + 1;

        document.getElementById('flyingArea').appendChild(flyingText);
        flyingTexts.push(flyingText);

        function move() {
            let currentLeft = parseFloat(flyingText.style.left);
            let currentTop = parseFloat(flyingText.style.top);

            if (currentLeft <= 0 || currentLeft >= 90) {
                flyingText.directionX *= -1;
            }
            if (currentTop <= 0 || currentTop >= 40) {
                flyingText.directionY *= -1;
            }

            flyingText.style.left = `${currentLeft + speed * flyingText.directionX}%`;
            flyingText.style.top = `${currentTop + speed * flyingText.directionY}vh`;
        }

        flyingText.directionX = direction;
        flyingText.directionY = direction;
        flyingText.moveInterval = setInterval(move, 50);
    }
}

function deleteOldestText() {
    if (flyingTexts.length > 0) {
        const oldestText = flyingTexts.shift();
        clearInterval(oldestText.moveInterval);
        oldestText.remove();
    }
}

function clearAllText() {
    while (flyingTexts.length > 0) {
        deleteOldestText();
    }
}
