function generateInputs() {
    const numSubjects = document.getElementById('numSubjects').value;
    const container = document.getElementById('subjectsContainer');
    container.innerHTML = ''; // 초기화

    for (let i = 0; i < numSubjects; i++) {
        const subjectDiv = document.createElement('div');
        subjectDiv.innerHTML = `
            <label>과목명:</label>
            <input type="text" class="subjectName"><br>
            <label>점수:</label>
            <input type="number" class="subjectScore" min="0" max="100"><br>
            <label>시수:</label>
            <input type="number" class="subjectCredit" min="0"><br><br>
        `;
        container.appendChild(subjectDiv);
    }
}

function calculateScores() {
    const scores = document.getElementsByClassName('subjectScore');
    const credits = document.getElementsByClassName('subjectCredit');
    let totalScore = 0, totalCredits = 0, totalWeightedScore = 0;

    for (let i = 0; i < scores.length; i++) {
        const score = parseFloat(scores[i].value);
        const credit = parseFloat(credits[i].value);

        totalScore += score;
        totalCredits += credit;
        totalWeightedScore += score * credit;
    }

    const averageScore = totalScore / scores.length;
    const universityScore = totalWeightedScore / totalCredits;

    document.getElementById('averageScore').innerText = '조졸조입성적: ' + averageScore.toFixed(2);
    document.getElementById('universityScore').innerText = '대학진학성적: ' + universityScore.toFixed(2);
}
