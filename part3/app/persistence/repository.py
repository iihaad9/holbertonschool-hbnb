from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.apply_update(data)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


class InMemoryRepository(Repository):
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_all(self):
        return list(self.storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        obj.apply_update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self.storage:
            del self.storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self.storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
