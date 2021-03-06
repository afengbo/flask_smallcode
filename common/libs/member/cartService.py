#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/25 11:31'

from application import app, db
from common.libs.Helper import get_current_time
from common.models.member.MemberCart import MemberCart


class CartService():
    @staticmethod
    def deleteItem(member_id=0, items=None):
        if member_id < 1 or not items:
            return False
        for item in items:
            MemberCart.query.filter_by(food_id=item['id'], member_id=member_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def setItems(member_id=0, food_id=0, number=0):
        if member_id < 1 or food_id < 1 or number < 1:
            return False

        cart_info = MemberCart.query.filter_by(member_id=member_id, food_id=food_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = MemberCart()
            model_cart.member_id = member_id
            model_cart.food_id = food_id
            model_cart.created_time = get_current_time()

        model_cart.quantity = number
        model_cart.updated_time = get_current_time()
        db.session.add(model_cart)
        db.session.commit()
        return True
