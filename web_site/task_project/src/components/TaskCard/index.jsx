import { Card } from 'antd';

function TaskCard({data}) {
  return (
    <Card title="Task" actionsBg='#cf9de8ff' style={{ width: 300}}>
      <p>ID: {data.id}</p>
      <p>Text: {data.text}</p>
      <p>Author: {data.author.name}</p>
    </Card>
  )
}

export default TaskCard
