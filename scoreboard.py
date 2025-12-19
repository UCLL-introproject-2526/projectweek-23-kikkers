import pygame
import os
import json

class Scoreboard:
    def __init__(self, x=10, y=10, font_size=32, font_name="Daydream_DEMO.ttf"):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font_name = font_name
        self.current_score = 0
        self.top_scores = self.load_top_scores()
        self.font = None
        self.final_score_added = False  # Track if final score was already added this session

    def set_font(self, font):
        """Set the font to use for rendering text"""
        self.font = font

    def load_top_scores(self):
        """Load top 5 scores from file"""
        try:
            scores_file = os.path.join('assets', 'top_scores.json')
            if os.path.exists(scores_file):
                with open(scores_file, 'r') as f:
                    return json.load(f)
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            pass
        return [0, 0, 0, 0, 0]  # Default top 5 scores

    def save_top_scores(self):
        """Save top 5 scores to file"""
        try:
            scores_file = os.path.join('assets', 'top_scores.json')
            os.makedirs(os.path.dirname(scores_file), exist_ok=True)
            with open(scores_file, 'w') as f:
                json.dump(self.top_scores, f)
        except Exception:
            pass  # Silently fail if we can't save

    def update_score(self, points):
        """Add points to current score (leaderboard updated separately at game over)"""
        self.current_score += points

    def add_final_score_to_leaderboard(self):
        """Add current score to leaderboard when game ends (only once per session)"""
        if not self.final_score_added and self.current_score > min(self.top_scores):
            self.top_scores.append(self.current_score)
            self.top_scores.sort(reverse=True)
            self.top_scores = self.top_scores[:5]  # Keep only top 5
            self.save_top_scores()
            self.final_score_added = True

    def reset_score(self):
        """Reset current score to 0 and prepare for new game session"""
        self.current_score = 0
        self.final_score_added = False

    def draw(self, screen):
        """Draw the current score during gameplay"""
        if self.font is None:
            # Fallback to system font if custom font not available
            self.font = pygame.font.SysFont(None, self.font_size)

        # Draw current score
        score_text = self.font.render(f"Score: {self.current_score}", True, (255, 100, 100))
        screen.blit(score_text, (self.x, self.y))

    def draw_top_scores(self, screen, x=None, y=None, title="TOP SCORES"):
        """Draw the top 5 scores scoreboard"""
        if self.font is None:
            self.font = pygame.font.SysFont(None, self.font_size)

        if x is None:
            x = screen.get_width() - 200  # Default to right side
        if y is None:
            y = 100  # Default vertical position

        # Draw title
        title_text = self.font.render(title, True, (255, 255, 0))
        screen.blit(title_text, (x, y))

        # Draw top 5 scores
        for i, score in enumerate(self.top_scores):
            if score > 0:  # Only show non-zero scores
                score_text = self.font.render(f"{i+1}. {score}", True, (255, 255, 255))
                screen.blit(score_text, (x, y + 40 + i * 30))

    def get_score(self):
        """Get current score"""
        return self.current_score

    def get_high_score(self):
        """Get the highest score (first in top_scores)"""
        return self.top_scores[0] if self.top_scores else 0

    def is_new_high_score(self, score):
        """Check if a score is a new high score"""
        return score > self.get_high_score()

    def get_score_position(self, score):
        """Get the position of a score in the top 5 (1-5), or 0 if not in top 5"""
        for i, top_score in enumerate(self.top_scores):
            if score >= top_score:
                return i + 1
        return 0
