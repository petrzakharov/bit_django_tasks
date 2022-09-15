from django.test import TestCase

from ..models import LeadState, Lead


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for attr in LeadState.__dict__.keys():
            if attr.startswith('STATE_'):
                setattr(
                    PostModelTest,
                    attr,
                    LeadState.objects.create(
                        name=str(getattr(LeadState, attr))
                    )
                )

    def test_correct_flow_new__in_progress(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_NEW,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_in_progress(), True)

    def test_correct_flow_in_progress__postponed(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_IN_PROGRESS,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_postponed(), True)

    def test_correct_flow_in_progress__done(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_IN_PROGRESS,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_done(), True)

    def test_correct_flow_postponed__in_progress(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_POSTPONED,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_in_progress(), True)

    def test_correct_flow_postponed__done(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_POSTPONED,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_done(), True)

    def test_wrong_flow_new__done(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_NEW,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_done(), False)

    def test_wrong_flow_done__in_progress(self):
        PostModelTest.lead = Lead.objects.create(
            state=PostModelTest.STATE_DONE,
            name='test'
        )
        self.assertEquals(PostModelTest.lead.make_state_in_progress(), False)
