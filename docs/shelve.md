# Структура данных в документе пользователя

```
{
  "userinfo": {
    "id": string # telegram id
    "name": string # telegram first name
    "username": string # telegram username
    "botnickname": string
    "year": number
    "department": string
    "groupnumber": string
  },
  "current_state": "default" | "on_start_scenario"
  "scenario_state": {
    "on_start_scenario"?: {
      "current_state": "waiting_create_profile"
    }
  }
}
```
