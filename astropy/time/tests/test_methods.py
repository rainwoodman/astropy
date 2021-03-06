# Licensed under a 3-clause BSD style license - see LICENSE.rst

# TEST_UNICODE_LITERALS
import itertools
import numpy as np

from .. import Time
from ...tests.helper import pytest
from ...utils.compat.numpycompat import NUMPY_LT_1_9

class TestManipulation():
    """Manipulation of Time objects, ensuring attributes are done correctly."""

    def setup(self):
        mjd = np.arange(50000, 50010)
        frac = np.arange(0., 0.999, 0.2)
        self.t0 = Time(mjd[:, np.newaxis] + frac, format='mjd', scale='utc')
        self.t1 = Time(mjd[:, np.newaxis] + frac, format='mjd', scale='utc',
                       location=('45d', '50d'))
        self.t2 = Time(mjd[:, np.newaxis] + frac, format='mjd', scale='utc',
                       location=(np.arange(len(frac)), np.arange(len(frac))))

    def test_ravel(self):
        t0_ravel = self.t0.ravel()
        assert t0_ravel.shape == (self.t0.size,)
        assert np.all(t0_ravel.jd1 == self.t0.jd1.ravel())
        assert np.may_share_memory(t0_ravel.jd1, self.t0.jd1)
        assert t0_ravel.location is None
        t1_ravel = self.t1.ravel()
        assert t1_ravel.shape == (self.t1.size,)
        assert np.all(t1_ravel.jd1 == self.t1.jd1.ravel())
        assert np.may_share_memory(t1_ravel.jd1, self.t1.jd1)
        assert t1_ravel.location is self.t1.location
        t2_ravel = self.t2.ravel()
        assert t2_ravel.shape == (self.t2.size,)
        assert np.all(t2_ravel.jd1 == self.t2.jd1.ravel())
        assert np.may_share_memory(t2_ravel.jd1, self.t2.jd1)
        assert t2_ravel.location.shape == t2_ravel.shape
        # Broadcasting and ravelling cannot be done without a copy.
        assert not np.may_share_memory(t2_ravel.location, self.t2.location)

    def test_flatten(self):
        t0_flatten = self.t0.flatten()
        assert t0_flatten.shape == (self.t0.size,)
        assert t0_flatten.location is None
        # Flatten always makes a copy.
        assert not np.may_share_memory(t0_flatten.jd1, self.t0.jd1)
        t1_flatten = self.t1.flatten()
        assert t1_flatten.shape == (self.t1.size,)
        assert not np.may_share_memory(t1_flatten.jd1, self.t1.jd1)
        assert t1_flatten.location is not self.t1.location
        assert t1_flatten.location == self.t1.location
        t2_flatten = self.t2.flatten()
        assert t2_flatten.shape == (self.t2.size,)
        assert not np.may_share_memory(t2_flatten.jd1, self.t2.jd1)
        assert t2_flatten.location.shape == t2_flatten.shape
        assert not np.may_share_memory(t2_flatten.location, self.t2.location)

    def test_transpose(self):
        t0_transpose = self.t0.transpose()
        assert t0_transpose.shape == (5, 10)
        assert np.all(t0_transpose.jd1 == self.t0.jd1.transpose())
        assert np.may_share_memory(t0_transpose.jd1, self.t0.jd1)
        assert t0_transpose.location is None
        t1_transpose = self.t1.transpose()
        assert t1_transpose.shape == (5, 10)
        assert np.all(t1_transpose.jd1 == self.t1.jd1.transpose())
        assert np.may_share_memory(t1_transpose.jd1, self.t1.jd1)
        assert t1_transpose.location is self.t1.location
        t2_transpose = self.t2.transpose()
        assert t2_transpose.shape == (5, 10)
        assert np.all(t2_transpose.jd1 == self.t2.jd1.transpose())
        assert np.may_share_memory(t2_transpose.jd1, self.t2.jd1)
        assert t2_transpose.location.shape == t2_transpose.shape
        assert np.may_share_memory(t2_transpose.location, self.t2.location)
        # Only one check on T, since it just calls transpose anyway.
        t2_T = self.t2.T
        assert t2_T.shape == (5, 10)
        assert np.all(t2_T.jd1 == self.t2.jd1.T)
        assert np.may_share_memory(t2_T.jd1, self.t2.jd1)
        assert t2_T.location.shape == t2_T.location.shape
        assert np.may_share_memory(t2_T.location, self.t2.location)

    def test_diagonal(self):
        t0_diagonal = self.t0.diagonal()
        assert t0_diagonal.shape == (5,)
        assert np.all(t0_diagonal.jd1 == self.t0.jd1.diagonal())
        assert t0_diagonal.location is None
        if not NUMPY_LT_1_9:
            assert np.may_share_memory(t0_diagonal.jd1, self.t0.jd1)
        t1_diagonal = self.t1.diagonal()
        assert t1_diagonal.shape == (5,)
        assert np.all(t1_diagonal.jd1 == self.t1.jd1.diagonal())
        assert t1_diagonal.location is self.t1.location
        if not NUMPY_LT_1_9:
            assert np.may_share_memory(t1_diagonal.jd1, self.t1.jd1)
        t2_diagonal = self.t2.diagonal()
        assert t2_diagonal.shape == (5,)
        assert np.all(t2_diagonal.jd1 == self.t2.jd1.diagonal())
        assert t2_diagonal.location.shape == t2_diagonal.shape
        if not NUMPY_LT_1_9:
            assert np.may_share_memory(t2_diagonal.jd1, self.t2.jd1)
            assert np.may_share_memory(t2_diagonal.location, self.t2.location)

    def test_swapaxes(self):
        t0_swapaxes = self.t0.swapaxes(0, 1)
        assert t0_swapaxes.shape == (5, 10)
        assert np.all(t0_swapaxes.jd1 == self.t0.jd1.swapaxes(0, 1))
        assert np.may_share_memory(t0_swapaxes.jd1, self.t0.jd1)
        assert t0_swapaxes.location is None
        t1_swapaxes = self.t1.swapaxes(0, 1)
        assert t1_swapaxes.shape == (5, 10)
        assert np.all(t1_swapaxes.jd1 == self.t1.jd1.swapaxes(0, 1))
        assert np.may_share_memory(t1_swapaxes.jd1, self.t1.jd1)
        assert t1_swapaxes.location is self.t1.location
        t2_swapaxes = self.t2.swapaxes(0, 1)
        assert t2_swapaxes.shape == (5, 10)
        assert np.all(t2_swapaxes.jd1 == self.t2.jd1.swapaxes(0, 1))
        assert np.may_share_memory(t2_swapaxes.jd1, self.t2.jd1)
        assert t2_swapaxes.location.shape == t2_swapaxes.shape
        assert np.may_share_memory(t2_swapaxes.location, self.t2.location)

    def test_reshape(self):
        t0_reshape = self.t0.reshape(5, 2, 5)
        assert t0_reshape.shape == (5, 2, 5)
        assert np.all(t0_reshape.jd1 == self.t0._time.jd1.reshape(5, 2, 5))
        assert np.all(t0_reshape.jd2 == self.t0._time.jd2.reshape(5, 2, 5))
        assert np.may_share_memory(t0_reshape.jd1, self.t0.jd1)
        assert np.may_share_memory(t0_reshape.jd2, self.t0.jd2)
        assert t0_reshape.location is None
        t1_reshape = self.t1.reshape(2, 5, 5)
        assert t1_reshape.shape == (2, 5, 5)
        assert np.all(t1_reshape.jd1 == self.t1.jd1.reshape(2, 5, 5))
        assert np.may_share_memory(t1_reshape.jd1, self.t1.jd1)
        assert t1_reshape.location is self.t1.location
        # For reshape(5, 2, 5), the location array can remain the same.
        t2_reshape = self.t2.reshape(5, 2, 5)
        assert t2_reshape.shape == (5, 2, 5)
        assert np.all(t2_reshape.jd1 == self.t2.jd1.reshape(5, 2, 5))
        assert np.may_share_memory(t2_reshape.jd1, self.t2.jd1)
        assert t2_reshape.location.shape == t2_reshape.shape
        assert np.may_share_memory(t2_reshape.location, self.t2.location)
        # But for reshape(5, 5, 2), location has to be broadcast and copied.
        t2_reshape2 = self.t2.reshape(5, 5, 2)
        assert t2_reshape2.shape == (5, 5, 2)
        assert np.all(t2_reshape2.jd1 == self.t2.jd1.reshape(5, 5, 2))
        assert np.may_share_memory(t2_reshape2.jd1, self.t2.jd1)
        assert t2_reshape2.location.shape == t2_reshape2.shape
        assert not np.may_share_memory(t2_reshape2.location, self.t2.location)
        t2_reshape_t = self.t2.reshape(10, 5).T
        assert t2_reshape_t.shape == (5, 10)
        assert np.may_share_memory(t2_reshape_t.jd1, self.t2.jd1)
        assert t2_reshape_t.location.shape == t2_reshape_t.shape
        assert np.may_share_memory(t2_reshape_t.location, self.t2.location)
        # Finally, reshape in a way that cannot be a view.
        t2_reshape_t_reshape = t2_reshape_t.reshape(10, 5)
        assert t2_reshape_t_reshape.shape == (10, 5)
        assert not np.may_share_memory(t2_reshape_t_reshape.jd1, self.t2.jd1)
        assert (t2_reshape_t_reshape.location.shape ==
                t2_reshape_t_reshape.shape)
        assert not np.may_share_memory(t2_reshape_t_reshape.location,
                                       t2_reshape_t.location)

    def test_shape_setting(self):
        t0_reshape = self.t0.copy()
        t0_reshape.shape = (5, 2, 5)
        assert t0_reshape.shape == (5, 2, 5)
        assert np.all(t0_reshape.jd1 == self.t0._time.jd1.reshape(5, 2, 5))
        assert np.all(t0_reshape.jd2 == self.t0._time.jd2.reshape(5, 2, 5))
        assert t0_reshape.location is None
        # But if the shape doesn't work, one should get an error.
        t0_reshape_t = t0_reshape.T
        with pytest.raises(AttributeError):
            t0_reshape_t.shape = (10, 5)
        t1_reshape = self.t1.copy()
        t1_reshape.shape = (2, 5, 5)
        assert t1_reshape.shape == (2, 5, 5)
        assert np.all(t1_reshape.jd1 == self.t1.jd1.reshape(2, 5, 5))
        # location is a single element, so its shape should not change.
        assert t1_reshape.location.shape == ()
        # For reshape(5, 2, 5), the location array can remain the same.
        t2_reshape = self.t2.copy()
        t2_reshape.shape = (5, 2, 5)
        assert t2_reshape.shape == (5, 2, 5)
        assert np.all(t2_reshape.jd1 == self.t2.jd1.reshape(5, 2, 5))
        assert t2_reshape.location.shape == t2_reshape.shape
        # But for reshape(5, 5, 2), location would need to be copied, so this
        # should fail.
        t2_reshape_t = t2_reshape.T
        with pytest.raises(AttributeError):
            t2_reshape_t.shape = (5, 5, 2)

    def test_squeeze(self):
        t0_squeeze = self.t0.reshape(5, 1, 2, 1, 5).squeeze()
        assert t0_squeeze.shape == (5, 2, 5)
        assert np.all(t0_squeeze.jd1 == self.t0.jd1.reshape(5, 2, 5))
        assert np.may_share_memory(t0_squeeze.jd1, self.t0.jd1)
        assert t0_squeeze.location is None
        t1_squeeze = self.t1.reshape(1, 5, 1, 2, 5).squeeze()
        assert t1_squeeze.shape == (5, 2, 5)
        assert np.all(t1_squeeze.jd1 == self.t1.jd1.reshape(5, 2, 5))
        assert np.may_share_memory(t1_squeeze.jd1, self.t1.jd1)
        assert t1_squeeze.location is self.t1.location
        t2_squeeze = self.t2.reshape(1, 1, 5, 2, 5, 1, 1).squeeze()
        assert t2_squeeze.shape == (5, 2, 5)
        assert np.all(t2_squeeze.jd1 == self.t2.jd1.reshape(5, 2, 5))
        assert np.may_share_memory(t2_squeeze.jd1, self.t2.jd1)
        assert t2_squeeze.location.shape == t2_squeeze.shape
        assert np.may_share_memory(t2_squeeze.location, self.t2.location)

    def test_add_dimension(self):
        t0_adddim = self.t0[:, np.newaxis, :]
        assert t0_adddim.shape == (10, 1, 5)
        assert np.all(t0_adddim.jd1 == self.t0.jd1[:, np.newaxis, :])
        assert np.may_share_memory(t0_adddim.jd1, self.t0.jd1)
        assert t0_adddim.location is None
        t1_adddim = self.t1[:, :, np.newaxis]
        assert t1_adddim.shape == (10, 5, 1)
        assert np.all(t1_adddim.jd1 == self.t1.jd1[:, :, np.newaxis])
        assert np.may_share_memory(t1_adddim.jd1, self.t1.jd1)
        assert t1_adddim.location is self.t1.location
        t2_adddim = self.t2[:, :, np.newaxis]
        assert t2_adddim.shape == (10, 5, 1)
        assert np.all(t2_adddim.jd1 == self.t2.jd1[:, :, np.newaxis])
        assert np.may_share_memory(t2_adddim.jd1, self.t2.jd1)
        assert t2_adddim.location.shape == t2_adddim.shape
        assert np.may_share_memory(t2_adddim.location, self.t2.location)

    def test_take(self):
        t0_take = self.t0.take((5, 2))
        assert t0_take.shape == (2,)
        assert np.all(t0_take.jd1 == self.t0._time.jd1.take((5, 2)))
        assert t0_take.location is None
        t1_take = self.t1.take((2, 4), axis=1)
        assert t1_take.shape == (10, 2)
        assert np.all(t1_take.jd1 == self.t1.jd1.take((2, 4), axis=1))
        assert t1_take.location is self.t1.location
        t2_take = self.t2.take((1, 3, 7), axis=0)
        assert t2_take.shape == (3, 5)
        assert np.all(t2_take.jd1 == self.t2.jd1.take((1, 3, 7), axis=0))
        assert t2_take.location.shape == t2_take.shape
        t2_take2 = self.t2.take((5, 15))
        assert t2_take2.shape == (2,)
        assert np.all(t2_take2.jd1 == self.t2.jd1.take((5, 15)))
        assert t2_take2.location.shape == t2_take2.shape


class TestArithmetic():
    """Arithmetic on Time objects, using both doubles."""
    kwargs = ({}, {'axis': None}, {'axis': 0}, {'axis': 1}, {'axis': 2})
    functions = ('min', 'max', 'sort')

    def setup(self):
        mjd = np.arange(50000, 50100, 10).reshape(2, 5, 1)
        frac = np.array([0.1, 0.1+1.e-15, 0.1-1.e-15, 0.9+2.e-16, 0.9])
        self.t0 = Time(mjd, frac, format='mjd', scale='utc')

        # Define arrays with same ordinal properties
        frac = np.array([1, 2, 0, 4, 3])
        self.t1 = Time(mjd + frac, format='mjd', scale='utc')
        self.jd = mjd + frac

    @pytest.mark.parametrize('kw, func', itertools.product(kwargs, functions))
    def test_argfuncs(self, kw, func):
        """
        Test that np.argfunc(jd, **kw) is the same as t0.argfunc(**kw) where
        jd is a similarly shaped array with the same ordinal properties but
        all integer values.  Also test the same for t1 which has the same
        integral values as jd.
        """
        t0v = getattr(self.t0, 'arg' + func)(**kw)
        t1v = getattr(self.t1, 'arg' + func)(**kw)
        jdv = getattr(np, 'arg' + func)(self.jd, **kw)
        assert np.all(t0v == jdv)
        assert np.all(t1v == jdv)
        assert t0v.shape == jdv.shape
        assert t1v.shape == jdv.shape

    @pytest.mark.parametrize('kw, func', itertools.product(kwargs, functions))
    def test_funcs(self, kw, func):
        """
        Test that np.func(jd, **kw) is the same as t1.func(**kw) where
        jd is a similarly shaped array and the same integral values.
        """
        t1v = getattr(self.t1, func)(**kw)
        jdv = getattr(np, func)(self.jd, **kw)
        assert np.all(t1v.value == jdv)
        assert t1v.shape == jdv.shape

    def test_argmin(self):
        assert self.t0.argmin() == 2
        assert np.all(self.t0.argmin(axis=0) == 0)
        assert np.all(self.t0.argmin(axis=1) == 0)
        assert np.all(self.t0.argmin(axis=2) == 2)

    def test_argmax(self):
        assert self.t0.argmax() == self.t0.size - 2
        assert np.all(self.t0.argmax(axis=0) == 1)
        assert np.all(self.t0.argmax(axis=1) == 4)
        assert np.all(self.t0.argmax(axis=2) == 3)

    def test_argsort(self):
        assert np.all(self.t0.argsort() == np.array([2, 0, 1, 4, 3]))
        assert np.all(self.t0.argsort(axis=0) == np.arange(2).reshape(2, 1, 1))
        assert np.all(self.t0.argsort(axis=1) == np.arange(5).reshape(5, 1))
        assert np.all(self.t0.argsort(axis=2) == np.array([2, 0, 1, 4, 3]))
        assert np.all(self.t0.argsort(axis=None) ==
                      np.arange(50).reshape(-1, 5)[:, (2, 0, 1, 4, 3)].ravel())

    def test_min(self):
        assert self.t0.min() == self.t0[0, 0, 2]
        assert np.all(self.t0.min(0) == self.t0[0])
        assert np.all(self.t0.min(1) == self.t0[:, 0])
        assert np.all(self.t0.min(2) == self.t0[:, :, 2])
        assert self.t0.min(0).shape == (5, 5)
        assert self.t0.min(0, keepdims=True).shape == (1, 5, 5)
        assert self.t0.min(1).shape == (2, 5)
        assert self.t0.min(1, keepdims=True).shape == (2, 1, 5)
        assert self.t0.min(2).shape == (2, 5)
        assert self.t0.min(2, keepdims=True).shape == (2, 5, 1)

    def test_max(self):
        assert self.t0.max() == self.t0[-1, -1, -2]
        assert np.all(self.t0.max(0) == self.t0[1])
        assert np.all(self.t0.max(1) == self.t0[:, 4])
        assert np.all(self.t0.max(2) == self.t0[:, :, 3])
        assert self.t0.max(0).shape == (5, 5)
        assert self.t0.max(0, keepdims=True).shape == (1, 5, 5)

    def test_ptp(self):
        assert self.t0.ptp() == self.t0.max() - self.t0.min()
        assert np.all(self.t0.ptp(0) == self.t0.max(0) - self.t0.min(0))
        assert self.t0.ptp(0).shape == (5, 5)
        assert self.t0.ptp(0, keepdims=True).shape == (1, 5, 5)

    def test_sort(self):
        assert np.all(self.t0.sort() == self.t0[:, :, (2, 0, 1, 4, 3)])
        assert np.all(self.t0.sort(0) == self.t0)
        assert np.all(self.t0.sort(1) == self.t0)
        assert np.all(self.t0.sort(2) == self.t0[:, :, (2, 0, 1, 4, 3)])
        assert np.all(self.t0.sort(None) ==
                      self.t0[:, :, (2, 0, 1, 4, 3)].ravel())
        # Bit superfluous, but good to check.
        assert np.all(self.t0.sort(-1)[:, :, 0] == self.t0.min(-1))
        assert np.all(self.t0.sort(-1)[:, :, -1] == self.t0.max(-1))
