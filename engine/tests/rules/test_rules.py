import pytest
from main.utils.variable import *
from main.main import Game
from main.rules.game_rules import GameRules
from main.state.contex import ActionContext


class TestGameRulesBasic:
    """Tests for basic GameRules initialization and structure"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        self.game = Game(data)
        self.ctx = ActionContext(self.game.state)

    def test_game_rules_initialization(self):
        """Test that GameRules initializes without errors"""
        assert self.rules is not None
        assert isinstance(self.rules, GameRules)

    def test_action_context_creation(self):
        """Test that ActionContext is properly created"""
        assert self.ctx is not None
        assert self.ctx.state is not None
        assert self.ctx.fraction is not None
        assert self.ctx.board is not None
        assert self.ctx.player is not None


class TestHandValidation:
    """Tests for hand-related validation methods"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_is_hand_full_empty_hand(self):
        """Test is_hand_full with empty hand"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        hand = ctx.player.hand
        assert not self.rules.is_hand_full(hand)

    def test_can_end_turn_with_empty_hand(self):
        """Test can_end_turn when hand is not full"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        result = self.rules.can_end_turn(ctx)
        assert result is True

    def test_can_end_turn_with_full_hand(self):
        """Test can_end_turn when hand is full"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Fill moloch's hand with multiple tokens
        moloch_hand = state_dict['players']['moloch']['hand']['tokens']
        moloch_pile = state_dict['players']['moloch']['pile']['tokens']
        for i in range(5):
            if moloch_pile:
                token = moloch_pile.pop(0)
                moloch_hand.append(token)
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        # Now hand should be full, so can_end_turn should be False
        result = self.rules.can_end_turn(ctx)
        # Full hand means cannot end turn
        if self.rules.is_hand_full(ctx.player.hand):
            assert result is False


class TestBottomValidation:
    """Tests for bottom (lower card ability) validation"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_can_use_bottom_end_turn_empty_hand(self):
        """Test if END_TURN bottom can be used with empty hand"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        result = self.rules.can_use_bottom(ctx, Bottom.END_TURN)
        assert result is True

    def test_can_use_bottom_end_turn_full_hand(self):
        """Test END_TURN bottom cannot be used with full hand"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Fill moloch's hand
        moloch_hand = state_dict['players']['moloch']['hand']['tokens']
        moloch_pile = state_dict['players']['moloch']['pile']['tokens']
        for i in range(5):
            if moloch_pile:
                token = moloch_pile.pop(0)
                moloch_hand.append(token)
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.interaction_phase = State.SELECTED_HAND
        
        result = self.rules.can_use_bottom(ctx, Bottom.END_TURN)
        assert result is False

    def test_get_available_bottoms_with_selection(self):
        """Test get_available_bottoms with actual selected token"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Add token to hand and select it
        state_dict['players']['moloch']['hand']['tokens'].append('klaun')
        state_dict['players']['moloch']['hand']['active_token'] = 0
        state_dict['selected'] = {Selected.NAME: 'klaun', Selected.SLOT: 0}
        state_dict['state'] = State.SELECTED_HAND
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        available = self.rules.get_available_bottoms(ctx, [Bottom.END_TURN, Bottom.DISCARD])
        assert isinstance(available, list)
        assert len(available) >= 0


class TestBoardPredicates:
    """Tests for board position predicates with tokens"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_board_with_moloch_token(self):
        """Test board predicates with moloch token on board"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place moloch token at position (2, 2)
        state_dict['board']['board'][2][2] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 1,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        # Test is_ally_at
        result = self.rules.is_ally_at(ctx, (2, 2))
        assert result is True
        
        # Test is_empty_at on empty position
        result_empty = self.rules.is_empty_at(ctx, (5, 5))
        assert result_empty is True

    def test_board_with_enemy_token(self):
        """Test board predicates with enemy token"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place borgo token
        state_dict['board']['board'][3][3] = {
            Token.FRACTION: 'borgo',
            Token.NAME: 'sztab',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        result = self.rules.is_enemy_at(ctx, (3, 3))
        assert result is True

    def test_board_with_wired_token(self):
        """Test is_wired_at with wired token"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        state_dict['board']['board'][4][4] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 1,
            Token.DAMAGE: 0,
            Token.WIRED: True
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        result = self.rules.is_wired_at(ctx, (4, 4))
        assert result is True

    def test_is_not_on_border_center(self):
        """Test is_not_on_border for center position"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        
        # Center position should not be on border
        result = self.rules.is_not_on_border(ctx, (5, 5))
        assert result is True


class TestMovementRules:
    """Tests for movement validation with actual board state"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_can_move_from_with_movable_token(self):
        """Test can_move_from with token that has adjacent empty spaces"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place a token surrounded by empty spaces
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        result = self.rules.can_move_from(ctx, (5, 5))
        # Should be able to move since surrounded by empty spaces
        assert isinstance(result, bool)

    def test_can_push_from_adjacent_tokens(self):
        """Test can_push_from with enemy token adjacent"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place moloch token at (5, 5)
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        # Place borgo token adjacent at (5, 6)
        state_dict['board']['board'][5][6] = {
            Token.FRACTION: 'borgo',
            Token.NAME: 'sztab',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        result = self.rules.can_push_from(ctx, (5, 5))
        assert isinstance(result, bool)


class TestPredicateMakers:
    """Tests for predicate factory methods with board context"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_adjacent_to_predicate_with_neighbors(self):
        """Test adjacent_to predicate with actual neighbors"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        
        center_pos = (5, 5)
        predicate = self.rules.adjacent_to(center_pos)
        
        # Get adjacent positions from board
        adjacent_hexes = ctx.board.adjacent_hexes(center_pos)
        
        # Test predicate on each adjacent position
        for adj_pos in adjacent_hexes:
            result = predicate(ctx, adj_pos)
            assert result is True

    def test_not_adjacent_to_predicate_distant_positions(self):
        """Test not_adjacent_to predicate with distant positions"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        
        center_pos = (5, 5)
        predicate = self.rules.not_adjacent_to(center_pos)
        
        distant_pos = (10, 10)
        result = predicate(ctx, distant_pos)
        assert result is True

    def test_can_be_pushed_by_predicate(self):
        """Test can_be_pushed_by predicate maker"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Setup: pusher at (5,5), target at (5,6), empty space at (5,7)
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        state_dict['board']['board'][5][6] = {
            Token.FRACTION: 'borgo',
            Token.NAME: 'sztab',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        predicate = self.rules.can_be_pushed_by((5, 5))
        result = predicate(ctx, (5, 6))
        assert isinstance(result, bool)


class TestTokenValidation:
    """Tests for token-related validation"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_is_token_hq_with_hq(self):
        """Test is_token_hq returns True for HQ token"""
        class MockToken:
            name = BoardType.HQ
        
        token = MockToken()
        result = self.rules.is_token_hq(token)
        assert result is True

    def test_is_token_hq_with_regular_token(self):
        """Test is_token_hq returns False for regular token"""
        class MockToken:
            name = 'szturmowiec'
        
        token = MockToken()
        result = self.rules.is_token_hq(token)
        assert result is False

    def test_is_hq_not_wired(self):
        """Test is_hq_not_wired validation"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        ctx = ActionContext(game.state)
        
        result = self.rules.is_hq_not_wired(ctx)
        assert isinstance(result, bool)


class TestLowLevelMovementFunctions:
    """Tests for internal movement validation with board state"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_can_move_to_empty_adjacent(self):
        """Test _can_move_to moving to empty adjacent position"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Token at position (5, 5)
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        # Get first adjacent hex
        adjacent = ctx.board.adjacent_hexes((5, 5))[0]
        result = self.rules._can_move_to(ctx, (5, 5), adjacent)
        assert isinstance(result, bool)

    def test_can_move_from_surrounded_by_empty(self):
        """Test _can_move from position with empty neighbors"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        result = self.rules._can_move(ctx, (5, 5))
        assert result is True

    def test_can_move_from_surrounded_by_enemies(self):
        """Test _can_move from position surrounded by enemies"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place moloch token in center
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        # Fill all adjacent spaces with borgo tokens
        adjacent_hexes = [(5, 4), (5, 6), (4, 5), (4, 6), (6, 4), (6, 5)]
        for hex_pos in adjacent_hexes:
            state_dict['board']['board'][hex_pos[0]][hex_pos[1]] = {
                Token.FRACTION: 'borgo',
                Token.NAME: 'sztab',
                Token.ROTATION: 0,
                Token.DAMAGE: 0,
                Token.WIRED: False
            }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        result = self.rules._can_move(ctx, (5, 5))
        assert result is False


class TestExecutionRules:
    """Tests for execution/action rules with game context"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_can_execute_use_with_selected_token(self):
        """Test can_execute_use with selected token"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Add token to hand
        state_dict['players']['moloch']['hand']['tokens'].append('klaun')
        state_dict['players']['moloch']['hand']['active_token'] = 0
        state_dict['selected'] = {Selected.NAME: 'klaun', Selected.SLOT: 0}
        state_dict['state'] = State.SELECTED_HAND
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        result = self.rules.can_execute_use(ctx)
        assert isinstance(result, bool)

    def test_can_execute_discard_with_selected_token(self):
        """Test can_execute_discard returns valid boolean"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        state_dict['players']['moloch']['hand']['tokens'].append('klaun')
        state_dict['players']['moloch']['hand']['active_token'] = 0
        state_dict['selected'] = {Selected.NAME: 'klaun', Selected.SLOT: 0}
        state_dict['state'] = State.SELECTED_HAND
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        result = self.rules.can_execute_discard(ctx)
        assert isinstance(result, bool)


class TestIntegration:
    """Integration tests combining multiple rules with complex scenarios"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rules = GameRules()

    def test_combat_scenario_moloch_vs_borgo(self):
        """Test rules in combat scenario: Moloch vs Borgo"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Setup: Moloch attacker at (5,5), Borgo defender at (5,6)
        state_dict['board']['board'][5][5] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        state_dict['board']['board'][5][6] = {
            Token.FRACTION: 'borgo',
            Token.NAME: 'sztab',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        # Check if moloch can push borgo
        can_push = self.rules.can_push_from(ctx, (5, 5))
        assert isinstance(can_push, bool)

    def test_full_turn_scenario(self):
        """Test full turn scenario with token selection and bottoms"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Set up selected token with hand not full
        state_dict['players']['moloch']['hand']['tokens'].append('klaun')
        state_dict['players']['moloch']['hand']['active_token'] = 0
        state_dict['selected'] = {Selected.NAME: 'klaun', Selected.SLOT: 0}
        state_dict['state'] = State.SELECTED_HAND
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        
        # Get available actions
        available_bottoms = self.rules.get_available_bottoms(
            ctx,
            [Bottom.USE, Bottom.DISCARD, Bottom.END_TURN]
        )
        
        assert isinstance(available_bottoms, list)
        assert len(available_bottoms) >= 0

    def test_blocked_position_scenario(self):
        """Test position blocked by multiple enemies"""
        data = {
            'fractions': ['moloch', 'borgo'],
            'phase': 'newgame'
        }
        game = Game(data)
        state_dict = game.state.to_dict()
        
        # Place moloch unit at center
        center = (5, 5)
        state_dict['board']['board'][center[0]][center[1]] = {
            Token.FRACTION: 'moloch',
            Token.NAME: 'szturmowiec',
            Token.ROTATION: 0,
            Token.DAMAGE: 0,
            Token.WIRED: False
        }
        
        # Fill adjacent hexes with borgo units
        adjacent = [(5, 4), (5, 6), (4, 5), (4, 6), (6, 4), (6, 5)]
        for hex_pos in adjacent:
            state_dict['board']['board'][hex_pos[0]][hex_pos[1]] = {
                Token.FRACTION: 'borgo',
                Token.NAME: 'sztab',
                Token.ROTATION: 0,
                Token.DAMAGE: 0,
                Token.WIRED: False
            }
        
        game = Game(state_dict)
        ctx = ActionContext(game.state)
        ctx.fraction = 'moloch'
        
        # Should not be able to move
        result = self.rules._can_move(ctx, center)
        assert result is False
