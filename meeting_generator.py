import random

participants = [
("tiangolo","Silent Architect"),
("dmontagu","Core Engineer"),
("Kludex","Mentor"),
("alejsdev","Feature Driver"),
("jaystone776","Firefighter"),
("YuriiMotov","Infra"),
("valentinDruzhinin","Security"),
("ceb10n","QA"),
("waynerv","DevOps"),
("tokusumi","Product Lead"),
("hasansezertasan","Frontend"),
("SwftAlpc","Mid Dev"),
("svlandeg","Research"),
("AlertRED","Tooling"),
("hard-coders","Business"),
("nilslindemann","Coordinator"),
("Zhongheng-Cheng","Junior Dev"),
("github-actions[bot]","Observer"),
("dependabot[bot]","Observer"),
("pre-commit-ci[bot]","Observer")
]


topic_bank = {
"auth": [
"auth service is failing under high load",
"token refresh flow needs redesign",
"login retries are causing cascading delays"
],
"infra": [
"Kubernetes pods are restarting frequently",
"memory leak suspected in one of the workers",
"autoscaling rules need adjustment"
],
"feature": [
"new onboarding flow proposal",
"dashboard redesign idea",
"AI assistant integration concept"
],
"testing": [
"test coverage dropped last sprint",
"regression bugs increasing",
"CI pipeline taking too long"
],
"security": [
"JWT expiry vulnerability",
"rate limiting missing in one endpoint",
"API key rotation policy"
]
}

role_style = {
"Silent Architect": [
"Root cause seems to be deeper in the auth middleware. The retry loop amplifies latency.",
"If we isolate the token service and introduce a circuit breaker, half these issues disappear.",
"The architecture is leaking state across sessions, that’s why these bugs repeat."
],
"Firefighter": [
"I fixed three blockers yesterday but two more came in overnight.",
"We need to stop feature work until this stabilizes.",
"This is on fire, production is not safe."
],
"Loud Router": [
"I think everyone should coordinate better.",
"We should probably schedule another meeting on this.",
"Let’s all sync once more after this call."
],
"Mentor": [
"I’ll pair up with Ishaan and walk through the module.",
"This part is confusing, let me explain it simply.",
"We’ve seen this pattern before, here’s how we fixed it."
],
"Product Lead": [
"Our priority is user login stability.",
"If this isn’t fixed, feature launch is blocked.",
"Let’s align this with next sprint goals."
],
"Manager": [
"We need clarity on ownership.",
"What is the delivery timeline?",
"Who is blocking whom?"
],
"Core Engineer": [
"The core service was not designed for this concurrency.",
"We may need to refactor the request pipeline.",
"This touches fundamental parts of the system."
],
"Feature Driver": [
"The new onboarding feature depends on this.",
"Ideally we shouldn’t pause everything.",
"I can decouple this if needed."
],
"QA": [
"Failure rate doubled in regression tests.",
"Most bugs point to auth instability.",
"I can’t certify this build."
],
"Security": [
"There is a vulnerability window here.",
"This needs a hotfix before release.",
"We’re violating one internal guideline."
],
"Infra": [
"Node memory keeps spiking.",
"Metrics show unusual container churn.",
"We can add monitoring but root cause is code."
],
"DevOps": [
"Deploy pipeline is failing intermittently.",
"Rollback took longer than expected.",
"We need better alerting."
],
"Frontend": [
"UI is breaking because sessions expire.",
"Users are getting logged out randomly.",
"Error handling is insufficient."
],
"Business": [
"This is impacting user trust.",
"We already got two partner complaints.",
"Delays affect roadmap promises."
],
"Coordinator": [
"I’ll document decisions.",
"I’ll track follow-ups.",
"I’ll sync notes after the call."
],
"Junior Dev": [
"I’m not fully sure where this fails.",
"Can someone explain the flow?",
"I can test a patch."
],
"Mid Dev": [
"I can take one module and stabilize it.",
"I’ll review the recent commits.",
"This seems related to yesterday’s merge."
],
"Research": [
"Similar issues appeared in distributed auth systems.",
"We can simulate this.",
"There’s an architectural pattern for this."
],
"Tooling": [
"Our debugging tools are weak here.",
"I can add tracing.",
"Logs are not sufficient."
],
"Observer": [
"Noted.",
"I’m following.",
"Understood."
]
}

def timestamp(sec):
    m = sec//60
    s = sec%60
    return f"[{m:02d}:{s:02d}]"

current_time = 0
lines = []

for i in range(420):   # ~50 minutes, ~420 speaking turns
    name, role = random.choice(participants)
    domain = random.choice(list(topic_bank.keys()))
    topic = random.choice(topic_bank[domain])
    style = random.choice(role_style[role])

    sentence = f"{style} ({topic})."
    lines.append(f"{timestamp(current_time)} {name}: {sentence}")

    current_time += random.randint(5,12)

with open("meeting_transcript.txt","w",encoding="utf-8") as f:
    for l in lines:
        f.write(l+"\n")

print("meeting_transcript.txt created (50 min realistic meeting)")
