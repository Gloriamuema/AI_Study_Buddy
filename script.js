// script.js
class StudyBuddyApp {
    constructor() {
        this.flashcards = [];
        this.currentIndex = 0;
        this.correctAnswers = new Set();
        this.incorrectAnswers = new Set();
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        document.getElementById('generate-btn').addEventListener('click', () => this.generateFlashcards());
        document.getElementById('current-flashcard').addEventListener('click', () => this.flipCard());
        document.getElementById('prev-btn').addEventListener('click', () => this.previousCard());
        document.getElementById('next-btn').addEventListener('click', () => this.nextCard());
        
        // Answer buttons
        document.querySelector('.correct-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.markAnswer(true);
        });
        
        document.querySelector('.incorrect-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.markAnswer(false);
        });
    }
    
    async generateFlashcards() {
        const notes = document.getElementById('study-notes').value;
        if (!notes.trim()) return;
        
        this.showLoading(true);
        
        try {
            const response = await fetch('http://localhost:5000/api/generate-flashcards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ notes })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.flashcards = data.flashcards;
                this.showFlashcards();
                this.updateCard();
            }
        } catch (error) {
            console.error('Error generating flashcards:', error);
            alert('Failed to generate flashcards. Please try again.');
        }
        
        this.showLoading(false);
    }
    
    showLoading(show) {
        const btnText = document.querySelector('.btn-text');
        const loader = document.querySelector('.loader');
        const btn = document.getElementById('generate-btn');
        
        if (show) {
            btnText.classList.add('hidden');
            loader.classList.remove('hidden');
            btn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            btn.disabled = false;
        }
    }
    
    showFlashcards() {
        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('flashcard-section').classList.remove('hidden');
    }
    
    updateCard() {
        const card = this.flashcards[this.currentIndex];
        document.getElementById('question-text').textContent = card.question;
        document.getElementById('answer-text').textContent = card.answer;
        document.getElementById('card-counter').textContent = `${this.currentIndex + 1} / ${this.flashcards.length}`;
        
        // Reset card to front
        document.getElementById('current-flashcard').classList.remove('flipped');
        
        this.updateProgress();
    }
    
    flipCard() {
        document.getElementById('current-flashcard').classList.toggle('flipped');
    }
    
    markAnswer(isCorrect) {
        const cardId = this.flashcards[this.currentIndex].id;
        
        if (isCorrect) {
            this.correctAnswers.add(cardId);
            this.incorrectAnswers.delete(cardId);
        } else {
            this.incorrectAnswers.add(cardId);
            this.correctAnswers.delete(cardId);
        }
        
        // Auto-advance to next card after a short delay
        setTimeout(() => {
            this.nextCard();
        }, 1000);
    }
    
    previousCard() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateCard();
        }
    }
    
    nextCard() {
        if (this.currentIndex < this.flashcards.length - 1) {
            this.currentIndex++;
            this.updateCard();
        }
    }
    
    updateProgress() {
        const progress = ((this.currentIndex + 1) / this.flashcards.length) * 100;
        document.querySelector('.progress-fill').style.width = `${progress}%`;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudyBuddyApp();
});
