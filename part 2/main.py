from app.persistence.repository import InMemoryRepository
from app.models.user import User

def main():
    repo = InMemoryRepository()
    User.set_repository(repo)

    u1 = User.create("Salman", "Al-Mutairi", "salman@email.com", "1234")
    print(u1.to_dict())

if __name__ == "__main__":
    main()
