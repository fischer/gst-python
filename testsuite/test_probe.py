# -*- Mode: Python; test-case-name: testsuite.test_probe -*-
# vi:si:et:sw=4:sts=4:ts=4

import sys
from common import gst, unittest

class ProbeTest(unittest.TestCase):
    def testWrongNumber(self):
        self.assertRaises(TypeError, gst.Probe, True)

    def testWrongType(self):
        # bool is int type
        self.assertRaises(TypeError, gst.Probe, "noint", lambda x: "x")
        # second arg should be callable
        self.assertRaises(TypeError, gst.Probe, True, "nocallable")

    def testPerformNoData(self):
        probe = gst.Probe(True, self._probe_callback, "yeeha")
        self.assertRaises(TypeError, probe.perform, None)
        self.assertRaises(TypeError, probe.perform, "nodata")

    def testPerformNoArg(self):
        probe = gst.Probe(True, self._probe_callback_no_arg)
        buffer = gst.Buffer()
        probe.perform(buffer)
        self.assertEqual(self._no_arg, None)

    def _probe_callback_no_arg(self, probe, data):
        self._no_arg = None

    def testPerformOneArg(self):
        probe = gst.Probe(True, self._probe_callback, "yeeha")
        buffer = gst.Buffer()
        probe.perform(buffer)
        self.assertEqual(self._probe_result, "yeeha")

    def _probe_callback(self, probe, data, result):
        self._probe_result = result
        return True

    def testPerformTwoArgs(self):
        probe = gst.Probe(True, self._probe_callback_two, "yeeha", "works")
        buffer = gst.Buffer()
        probe.perform(buffer)
        self.assertEqual(self._probe_result1, "yeeha")
        self.assertEqual(self._probe_result2, "works")

    def _probe_callback_two(self, probe, data, result1, result2):
        self._probe_result1 = result1
        self._probe_result2 = result2
        return True
    
    # this test checks if the probe can replace the probed GstData with
    # another, FIXME: use return values on probe callback for this
    def notestPerformChangeBuffer(self):
        probe = gst.Probe(True, self._probe_callback_change_buffer)
        buffer = gst.Buffer('changeme')
        probe.perform(buffer)
        self.assertEqual(str(buffer), 'changed')

    def _probe_callback_change_buffer(self, probe, data):
        data = gst.Buffer('changed')
 
    def testFakeSrcProbe(self):
        pipeline = gst.Pipeline()
        fakesrc = gst.element_factory_make('fakesrc')
        fakesrc.set_property('num-buffers', 1)
        fakesink = gst.element_factory_make('fakesink')

        pipeline.add_many(fakesrc, fakesink)
        fakesrc.link(fakesink)
        pad = fakesrc.get_pad('src')
        probe = gst.Probe(True, self._probe_callback_fakesrc)
        pad.add_probe(probe)
        pipeline.set_state(gst.STATE_PLAYING)
        while pipeline.iterate(): pass
        self.assertEqual(self._got_fakesrc_buffer, True)

    def _probe_callback_fakesrc(self, probe, data):
        self._got_fakesrc_buffer = True

if __name__ == "__main__":
    unittest.main()
