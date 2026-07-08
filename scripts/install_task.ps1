$taskName="Social Media Analytics"

$action=New-ScheduledTaskAction `
-Execute "$env:USERPROFILE\Documents\Automation\social-media-analytics-automation\scripts\run_social_media_analytics.bat"

$monthlyTrigger=New-ScheduledTaskTrigger `
-Monthly `
-DaysOfMonth 1 `
-At 09:00

$startupTrigger=New-ScheduledTaskTrigger `
-AtLogOn

$settings=New-ScheduledTaskSettingsSet `
-StartWhenAvailable `
-MultipleInstances IgnoreNew

Register-ScheduledTask `
-TaskName $taskName `
-Action $action `
-Trigger @(
    $monthlyTrigger,
    $startupTrigger
) `
-Settings $settings `
-Force