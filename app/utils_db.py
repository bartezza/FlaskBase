
import copy
from .utils import new_id


class ModelDb:
    # _coll
    _data: dict
    _is_new: bool

    @property
    def id(self):
        return self._data["id"]

    @property
    def is_new(self):
        return self._is_new

    def __init__(self, coll, data, is_new):
        self._coll = coll
        self._data = data
        self._is_new = is_new

    @classmethod
    def get_by_id(cls, coll, id):
        ret = coll.find_one({"id": id})
        if ret is not None:
            return cls(coll=coll, data=ret, is_new=False)
        else:
            return None

    @classmethod
    def find(cls, coll, query={}, sort=None):
        data = coll.find(query)
        if sort is not None:
            data = data.sort(sort)
        poss = []
        for pos_data in data:
            poss.append(cls(coll=coll, data=pos_data, is_new=False))
        return poss

    def duplicate(self):
        other = self.__class__(coll=self._coll, data=copy.deepcopy(self._data), is_new=True)
        other._data["id"] = new_id()
        return other

    def update_db(self):
        if self._is_new:
            self._coll.insert_one(self._data)
        else:
            res = self._coll.update_one(
                {"_id": self._data["_id"]},
                {"$set": self._data}
            )
            if res.matched_count != 1:
                raise Exception("No match while updating {} ({})".format(self.__class__.__name__, self._data["id"]))

    def delete_db(self):
        # self.coll.delete_one({"_id": bson.objectid.ObjectId(_id)})
        self._coll.delete_one({"_id": self._data["_id"]})
