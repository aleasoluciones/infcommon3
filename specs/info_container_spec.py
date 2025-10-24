from mamba import description, context, it
from expects import expect, equal, be, raise_error, contain
import pickle

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

    with context('passing a tuple'):
        with it('returns an object'):
            container = InfoContainer(
                ({'key1': 'value1'}, {'key2': 'value2'}))

            expect(container[0].key1).to(equal('value1'))
            expect(container[1].key2).to(equal('value2'))

        with it('has length'):
            container = InfoContainer(('value0', 'value1'))

            expect(len(container)).to(equal(2))

        with it('is iterable'):
            container = InfoContainer(('value0', 'value1'))

            expect([element for element in container]).to(equal(['value0', 'value1']))

    with context('testing equality'):
        with it('two containers with same data are equal'):
            container1 = InfoContainer({'key1': 'value1', 'key2': 'value2'})
            container2 = InfoContainer({'key1': 'value1', 'key2': 'value2'})

            expect(container1 == container2).to(be(True))
            expect(container1).to(equal(container2))

        with it('two containers with different data are not equal'):
            container1 = InfoContainer({'key1': 'value1'})
            container2 = InfoContainer({'key1': 'value2'})

            expect(container1 == container2).to(be(False))
            expect(container1 != container2).to(be(True))

        with it('container is not equal to non-container object'):
            container = InfoContainer({'key1': 'value1'})

            expect(container == {'key1': 'value1'}).to(be(False))
            expect(container != {'key1': 'value1'}).to(be(True))

    with context('testing string representation'):
        with it('returns a formatted string representation'):
            container = InfoContainer({'key1': 'value1'})

            representation = repr(container)
            expect(representation).to(contain('key1'))
            expect(representation).to(contain('value1'))

    with context('accessing items with getitem'):
        with it('can access dict items by string key'):
            container = InfoContainer({'key1': 'value1', 'key2': 'value2'})

            expect(container['key1']).to(equal('value1'))
            expect(container['key2']).to(equal('value2'))

        with it('can access list items by integer index'):
            container = InfoContainer([{'key1': 'value1'}, {'key2': 'value2'}])

            expect(container[0].key1).to(equal('value1'))
            expect(container[1].key2).to(equal('value2'))

    with context('serialization with pickle'):
        with it('can be pickled and unpickled'):
            original = InfoContainer({'key1': 'value1', 'key2': {'key2_1': 'value2_1'}})

            pickled = pickle.dumps(original)
            restored = pickle.loads(pickled)

            expect(restored.key1).to(equal('value1'))
            expect(restored.key2.key2_1).to(equal('value2_1'))
            expect(restored).to(equal(original))

        with it('can pickle a list container'):
            original = InfoContainer(['value0', {'key1': 'value1'}])

            pickled = pickle.dumps(original)
            restored = pickle.loads(pickled)

            expect(restored[0]).to(equal('value0'))
            expect(restored[1].key1).to(equal('value1'))
            expect(len(restored)).to(equal(2))

    with context('edge cases'):
        with it('handles None values'):
            container = InfoContainer({'key1': None, 'key2': 'value2'})

            expect(container.key1).to(be(None))
            expect(container.key2).to(equal('value2'))

        with it('handles empty strings'):
            container = InfoContainer({'key1': '', 'key2': 'value2'})

            expect(container.key1).to(equal(''))
            expect(container.key2).to(equal('value2'))

        with it('handles nested tuples in dict values'):
            container = InfoContainer({'key1': ('a', 'b', 'c')})

            expect(container.key1).to(equal(['a', 'b', 'c']))

        with it('handles complex nested structures'):
            container = InfoContainer({
                'level1': {
                    'level2': {
                        'level3': 'deep_value'
                    }
                }
            })

            expect(container.level1.level2.level3).to(equal('deep_value'))

        with it('handles numeric keys as strings when accessing dict'):
            container = InfoContainer({'1': 'value1', '2': 'value2'})

            expect(container['1']).to(equal('value1'))

        with it('handles boolean values'):
            container = InfoContainer({'key1': True, 'key2': False})

            expect(container.key1).to(be(True))
            expect(container.key2).to(be(False))

        with it('preserves return_none in nested containers'):
            container = InfoContainer({'nested': {'key1': 'value1'}}, return_none=True)

            expect(container.nested.nonexistent).to(be(None))
            expect(container.nonexistent).to(be(None))
