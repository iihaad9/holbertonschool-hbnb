from app.persistence.repository import InMemoryRepository
from app.models.user import User

def main():
    print("MAIN STARTED ✅")

    repo = InMemoryRepository()
    User.set_repository(repo)

    u1 = User.create("Salman", "Al-Mutairi", "s@email.com", "1234")
    u2 = User.create("salwa","fares","sss@gmail.com.com",1234)
    print("Created:", u1.to_dict())

    print("All users:", [u.to_dict() for u in User.get_all()])

if __name__ == "__main__":
    main()
