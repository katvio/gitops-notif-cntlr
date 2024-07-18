Event-driven GitOps custom notification controller.
Basically a FlaskAPI that receives Webhooks json payload from Github (for each commits made by Fluxcd/Argocd), checks that the new Docker image is running fine in a newly created pod, and sends custom notifications to Slack channel to inform Devs that their deployment is now live or in the monitoring channel.
