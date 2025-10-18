import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import type { TopUser } from "@/types/api";

interface TopUsersCardProps {
  users: TopUser[];
}

export function TopUsersCard({ users }: TopUsersCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Users</CardTitle>
        <p className="text-sm text-muted-foreground">
          Most active users by message count
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {users.map((user, index) => (
            <div key={user.user_id}>
              <div className="flex items-center gap-4">
                <Avatar>
                  <AvatarFallback>
                    {String(user.user_id).slice(-2)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium leading-none">
                    User {user.user_id}
                  </p>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-xs">
                      {user.messages_count} messages
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      {user.conversations_count} conversations
                    </Badge>
                  </div>
                </div>
                <div className="text-2xl font-bold text-muted-foreground">
                  #{index + 1}
                </div>
              </div>
              {index < users.length - 1 && <Separator className="mt-4" />}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
