from soma.workflow.client import Job, Workflow, WorkflowController, FileTransfer
from soma.workflow.client import Helper

# FileTransfer creation for input files
myfile = FileTransfer(is_input=True,
                    client_path="/tmp/soma_workflow_examples/myfile",
                    name="myfile")

# FileTransfer creation for output files
copy_of_myfile = FileTransfer(is_input=False,
                              client_path="/tmp/soma_workflow_examples/copy_of_myfile",
                              name="copy of my file")

# Job and Workflow
copy_job = Job(command=["cp", myfile, copy_of_myfile],
              name="copy",
              referenced_input_files=[myfile],
              referenced_output_files=[copy_of_myfile])

workflow = Workflow(jobs=[copy_job],
                    dependencies=[])

# submit the workflow
controller = WorkflowController("jinpeng-Latitude-E6530", "jinpeng")

wf_id = controller.submit_workflow(workflow=workflow,
                          name="simple transfer")

Helper.transfer_input_files(wf_id, controller)
Helper.wait_workflow(wf_id, controller)
Helper.transfer_output_files(wf_id, controller)
controller.delete_workflow(wf_id)