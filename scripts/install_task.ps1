$taskName="Social Media Analytics"

$projectPath="$env:USERPROFILE\Documents\Automation\social-media-analytics-automation"

$action=New-ScheduledTaskAction `
-Execute "$projectPath\scripts\run_social_media_analytics.bat"

$trigger1=New-ScheduledTaskTrigger `
-Monthly `
-DaysOfMonth 1 `
-At 09:00

$trigger2=New-ScheduledTaskTrigger `
-AtLogOn

$settings=New-ScheduledTaskSettingsSet `
-StartWhenAvailable `
-MultipleInstances IgnoreNew `
-AllowStartIfOnBatteries `
-DontStopIfGoingOnBatteries

Register-ScheduledTask `
-TaskName $taskName `
-Action $action `
-Trigger @(
    $trigger1,
    $trigger2
) `
-Settings $settings `
-Description "Social Media Analytics Automation" `
-Force