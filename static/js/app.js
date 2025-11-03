// Course Selection AI Analyzer - Frontend JavaScript

// State Management
const state = {
    courses: [],
    answers: [],
    interestScores: {},
    requirements: {},
    currentStep: 1
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabSwitching();
    initUpload();
    initGPACalculator();
});

// Tab Switching
function initTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;

            // Update active states
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Upload Functionality
function initUpload() {
    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('pdf-upload');
    const useSampleBtn = document.getElementById('use-sample-btn');

    // Click to upload
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'var(--primary)';
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.borderColor = 'var(--border)';
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'var(--border)';
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileUpload(file);
        } else {
            showStatus('Please upload a PDF file', 'error');
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Use sample data
    useSampleBtn.addEventListener('click', useSampleData);
}

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('pdf', file);

    showLoading(true);

    try {
        const response = await fetch('/upload-pdf', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            state.courses = data.courses;
            showStatus(`Successfully loaded ${data.count} courses!`, 'success');
            setTimeout(() => loadQuestions(), 1000);
        } else {
            showStatus(data.error || 'Failed to parse PDF', 'error');
        }
    } catch (error) {
        showStatus('Error uploading file: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function useSampleData() {
    showLoading(true);

    try {
        const response = await fetch('/use-sample-data', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            state.courses = data.courses;
            showStatus(`Loaded ${data.count} sample courses!`, 'success');
            setTimeout(() => loadQuestions(), 1000);
        } else {
            showStatus('Failed to load sample data', 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Questions
async function loadQuestions() {
    try {
        const response = await fetch('/get-questions');
        const data = await response.json();

        const container = document.getElementById('questions-container');
        container.innerHTML = '';

        data.questions.forEach((q, index) => {
            const questionCard = createQuestionCard(q, index);
            container.appendChild(questionCard);
        });

        document.getElementById('upload-section').classList.add('hidden');
        document.getElementById('questions-section').classList.remove('hidden');
        document.getElementById('submit-answers-btn').classList.remove('hidden');

        // Setup submit button
        document.getElementById('submit-answers-btn').addEventListener('click', submitAnswers);
    } catch (error) {
        showStatus('Error loading questions: ' + error.message, 'error');
    }
}

function createQuestionCard(question, index) {
    const card = document.createElement('div');
    card.className = 'question-card';

    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    questionText.textContent = `${index + 1}. ${question.question}`;

    const optionsDiv = document.createElement('div');
    optionsDiv.className = 'question-options';

    question.options.forEach(option => {
        const optionBtn = document.createElement('button');
        optionBtn.className = 'option-btn';
        optionBtn.textContent = option.charAt(0).toUpperCase() + option.slice(1);
        optionBtn.dataset.questionId = question.id;
        optionBtn.dataset.answer = option;

        optionBtn.addEventListener('click', () => {
            // Deselect other options for this question
            optionsDiv.querySelectorAll('.option-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            optionBtn.classList.add('selected');

            // Update state
            const existingIndex = state.answers.findIndex(a => a.question_id === question.id);
            if (existingIndex >= 0) {
                state.answers[existingIndex] = { question_id: question.id, answer: option };
            } else {
                state.answers.push({ question_id: question.id, answer: option });
            }
        });

        optionsDiv.appendChild(optionBtn);
    });

    card.appendChild(questionText);
    card.appendChild(optionsDiv);

    return card;
}

async function submitAnswers() {
    if (state.answers.length === 0) {
        showStatus('Please answer at least one question', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/submit-answers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: state.answers })
        });

        const data = await response.json();

        if (data.success) {
            state.interestScores = data.interest_scores;
            showRequirements();
        } else {
            showStatus('Failed to process answers', 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Requirements
function showRequirements() {
    document.getElementById('questions-section').classList.add('hidden');
    document.getElementById('requirements-section').classList.remove('hidden');

    document.getElementById('submit-requirements-btn').addEventListener('click', submitRequirements);
}

async function submitRequirements() {
    const requirements = {
        total_credits: parseInt(document.getElementById('total-credits').value) || 120,
        completed_credits: parseInt(document.getElementById('completed-credits').value) || 0,
        'Computer Science': parseInt(document.getElementById('req-cs').value) || 0,
        'Mathematics': parseInt(document.getElementById('req-math').value) || 0,
        'English': parseInt(document.getElementById('req-english').value) || 0,
        'Physics': parseInt(document.getElementById('req-physics').value) || 0,
        'History': parseInt(document.getElementById('req-history').value) || 0,
        'Art': parseInt(document.getElementById('req-art').value) || 0
    };

    showLoading(true);

    try {
        // Submit requirements
        await fetch('/submit-requirements', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ requirements })
        });

        // Get recommendations
        const response = await fetch('/get-recommendations', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showRecommendations(data.recommendations);
        } else {
            showStatus(data.error || 'Failed to get recommendations', 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Recommendations
function showRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    container.innerHTML = '';

    recommendations.forEach((rec, index) => {
        const card = createRecommendationCard(rec, index + 1);
        container.appendChild(card);
    });

    document.getElementById('requirements-section').classList.add('hidden');
    document.getElementById('recommendations-section').classList.remove('hidden');

    // Restart button
    document.getElementById('restart-btn').addEventListener('click', () => {
        location.reload();
    });
}

function createRecommendationCard(rec, rank) {
    const card = document.createElement('div');
    card.className = 'recommendation-card';

    card.innerHTML = `
        <div class="recommendation-header">
            <div class="recommendation-rank">#${rank}</div>
            <div class="recommendation-score">Score: ${rec.score.toFixed(1)}</div>
        </div>
        <h3 class="recommendation-title">${rec.name}</h3>
        <div class="recommendation-code">${rec.code}</div>
        ${rec.description ? `<p class="recommendation-description">${rec.description}</p>` : ''}
        <div class="recommendation-reasons">
            ${rec.reasons.map(reason => `
                <div class="reason-item">
                    <svg class="reason-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>${reason}</span>
                </div>
            `).join('')}
        </div>
    `;

    return card;
}

// GPA Calculator
function initGPACalculator() {
    const addBtn = document.getElementById('add-grade-btn');
    const calculateBtn = document.getElementById('calculate-gpa-btn');

    addBtn.addEventListener('click', addGradeEntry);
    calculateBtn.addEventListener('click', calculateGPA);

    // Setup initial remove button
    setupRemoveButtons();
}

function addGradeEntry() {
    const container = document.getElementById('grades-container');
    const newEntry = document.createElement('div');
    newEntry.className = 'grade-entry';
    newEntry.innerHTML = `
        <div class="form-group">
            <label>Course Name</label>
            <input type="text" class="course-name form-input" placeholder="e.g., CS101">
        </div>
        <div class="form-group">
            <label>Grade</label>
            <select class="course-grade form-input">
                <option value="A+">A+</option>
                <option value="A">A</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B">B</option>
                <option value="B-">B-</option>
                <option value="C+">C+</option>
                <option value="C">C</option>
                <option value="C-">C-</option>
                <option value="D+">D+</option>
                <option value="D">D</option>
                <option value="D-">D-</option>
                <option value="F">F</option>
            </select>
        </div>
        <div class="form-group">
            <label>Credits</label>
            <input type="number" class="course-credits form-input" value="3" min="0" step="0.5">
        </div>
        <button class="btn-icon remove-grade-btn" title="Remove course">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
        </button>
    `;
    container.appendChild(newEntry);
    setupRemoveButtons();
}

function setupRemoveButtons() {
    const removeButtons = document.querySelectorAll('.remove-grade-btn');
    removeButtons.forEach(btn => {
        btn.onclick = () => {
            const container = document.getElementById('grades-container');
            if (container.children.length > 1) {
                btn.closest('.grade-entry').remove();
            }
        };
    });
}

async function calculateGPA() {
    const entries = document.querySelectorAll('.grade-entry');
    const grades = [];

    entries.forEach(entry => {
        const grade = entry.querySelector('.course-grade').value;
        const credits = parseFloat(entry.querySelector('.course-credits').value) || 0;

        if (credits > 0) {
            grades.push({ grade, credits });
        }
    });

    if (grades.length === 0) {
        showStatus('Please add at least one course with credits', 'error');
        return;
    }

    const currentGPA = parseFloat(document.getElementById('current-gpa').value) || 0;
    const currentCredits = parseFloat(document.getElementById('current-credits').value) || 0;

    try {
        const response = await fetch('/calculate-gpa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                grades,
                current_gpa: currentGPA,
                current_credits: currentCredits
            })
        });

        const data = await response.json();

        if (data.success) {
            displayGPAResults(data.result);
        } else {
            showStatus('Failed to calculate GPA', 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

function displayGPAResults(result) {
    const resultsDiv = document.getElementById('gpa-results');
    resultsDiv.classList.remove('hidden');

    document.getElementById('semester-gpa').textContent = 
        (result.semester_gpa || result.gpa).toFixed(2);
    document.getElementById('cumulative-gpa').textContent = 
        (result.cumulative_gpa || result.gpa).toFixed(2);
    document.getElementById('total-credits-result').textContent = 
        result.total_credits;

    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Utility Functions
function showStatus(message, type) {
    const statusDiv = document.getElementById('upload-status');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    
    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'status-message';
    }, 5000);
}

function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}
