# -*- coding: utf-8 -*-

from mamba import description, context, it
from expects import expect, equal, be, raise_error

from infcommon.info_container.info_container import InfoContainer


with description('Info Container'):
    with context('passing a dictionary'):
        with it('returns an object'):
            container = InfoContainer(
                dict(key1='value1',
                    key2={'key2_1': 'value2_1'},
                    key3=5,
                    key4=[1, 'irrelevant']))

            expect(container.key1).to(equal('value1'))
            expect(container.key2.key2_1).to(equal('value2_1'))
            expect(container.key3).to(equal(5))
            expect(container.key4).to(equal([1, 'irrelevant']))

        with it('is iterable over empty info container'):
            container = InfoContainer(dict())

            expect([element for element in container]).to(equal([{}]))

    with context('passing a sequence'):
        with it('returns an object'):
            container = InfoContainer(
                dict(key1=[{'key1_1': 'value1_1', 'key1_2': 'value1_2'},
                           {'key2_1': 'value2_1', 'key2_2': 'value2_2'}]))

            expect(container.key1[0].key1_1).to(equal('value1_1'))

    with context('passing a list'):
        with it('is a list'):
            container = InfoContainer([{
                                                     'key1_1': 'value1_1', 'key1_2': 'value1_2'}])

            expect(container.is_list()).to(be(True))

        with it('can access info by index'):
            container = InfoContainer(['value pos 0', {'key1': 'value1'}])

            expect(container[0]).to(equal('value pos 0'))
            expect(container[1].key1).to(equal('value1'))

        with it('has length'):
            container = InfoContainer(['value pos 0', {'key1': 'value1'}])

            expect(len(container)).to(equal(2))

        with it('is iterable'):
            container = InfoContainer(['value0', 'value1'])

            expect([element for element in container]).to(equal(['value0', 'value1']))

        with it('is iterable over empty info container'):
            container = InfoContainer([])

            expect([element for element in container]).to(equal([]))

    with context('setting return_none as True'):
        with context('while asking for a key that is not available'):
            with it('returns None'):
                container = InfoContainer(dict(), return_none=True)

                expect(container.key1).to(be(None))

    with context('asking for a key that is not available'):
        with it('raise an Exception'):
            container = InfoContainer(dict())

            def _ask_container_for_key():
                container.key1

            expect(_ask_container_for_key).to(raise_error(AttributeError))

    with context('asking for data'):
        with it('returns it'):
            container = InfoContainer({'key1': 'value1', 'key2': 'value2'})

            expect(container.data()).to(equal({'key1': 'value1', 'key2': 'value2'}))
