
class TetrashopKnowledge:
    REPOSITORIES = {
        'repo_1': {'url': 'https://github.com/tetrashop/repo1', 'type': 'microservice'},
        'repo_2': {'url': 'https://github.com/tetrashop/repo2', 'type': 'database'}
    }
    
    UPDATE_STRATEGIES = {
        'breaking_changes': 'sequential',
        'minor_updates': 'parallel'
    }

print("✅ دانش تتراشاپ بارگذاری شد")
