## Script (Python) "guard_submit_analysis"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

wf_tool = context.portal_workflow

analyses = ['Analysis', 'DuplicateAnalysis', 'ReferenceAnalysis']

if context.portal_type in analyses:
    # For now, more thorough than strictly needed.
    if not context.getAttachment():
        service = context.getService()
        if service.getAttachmentOption() == 'r':
            return False
    dependencies = context.getDependencies()
    if dependencies:
        interim_fields = False
        service = context.getService()
        calculation = service.getCalculation()
        if calculation:
            interim_fields = calculation.getInterimFields()
        for dep in dependencies:
            review_state = wf_tool.getInfoFor(dep, 'review_state')
            if interim_fields:
                if review_state in ('sample_due', 'sample_received', 'attachment_due', 'to_be_verified',):
                    return False
            else:
                if review_state in ('sample_due', 'sample_received', 'attachment_due',):
                    return False
    return True
elif context.portal_type == 'AnalysisRequest':
    # Only transition to 'to_be_verified' if all analyses are at least there.
    for a in context.objectValues('Analysis'):
        review_state = wf_tool.getInfoFor(a, 'review_state')
        if review_state in ('sample_due', 'sample_received', 'attachment_due'):
            return False
    return True
