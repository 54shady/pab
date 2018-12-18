#!/usr/bin/env python
# coding=utf-8

import sys


class SingleListNode():
    def __init__(self, data, action=None):
        self.data = data
        self.next = None
        self.build_action = action

    def __str__(self):
        return self.data


class SingleList():
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.len = 0
        self.default_actionall = 0

    def list_len(self):
        return self.len

    def insert_node_front(self, data, action):
        node = SingleListNode(data, action)
        node.next = self.head
        self.head = node
        self.len += 1

    def append_node_rear(self, data, action):
        node = SingleListNode(data, action)
        # insert first node
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.len += 1

    def traverse(self, handler, **kwargs):
        iterator = self.head
        # if we got key, which means need search
        has_key = kwargs.has_key('key')
        while iterator:
            # search node case
            if has_key:
                ret = handler(iterator, kwargs.get('key'))
                if ret:
                    return ret
                else:
                    pass
            # normal case
            else:
                handler(iterator)
            iterator = iterator.next
        return None

    def print_data(self, node):
        print node.data,

    def run_action(self, node):
        if node.data:
            self.default_actionall += 1
            node.build_action()

    def do_command(self):
        self.traverse(self.run_action)

    def show_datas(self):
        self.traverse(self.print_data)
        print '\n'
