import discord
from discord.ext import commands
import os

# إعدادات الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# كلاس قائمة اختيار التكتات
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="تكت شراء", description="لعمليات الشراء والطلبات", emoji="💰"),
            discord.SelectOption(label="تكت استفسار", description="لأي سؤال أو استفسار لديك", emoji="❓")
        ]
        super().__init__(placeholder="اختر نوع التكت...", options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        ticket_type = self.values[0]
        guild = interaction.guild
        
        # ضبط صلاحيات القناة: المسؤول والعميل فقط من يرى القناة
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # إنشاء القناة
        channel = await guild.create_text_channel(
            name=f"{ticket_type}-{interaction.user.name}",
            overwrites=overwrites
        )
        
        await interaction.response.send_message(f"تم فتح {ticket_type} لك: {channel.mention}", ephemeral=True)
        await channel.send(f"أهلاً {interaction.user.mention}، لقد اخترت {ticket_type}. الإدارة ستصلك قريباً!")

# كلاس الـ View الذي يحتوي القائمة
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# تشغيل البوت عند الجاهزية
@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f'البوت {bot.user} يعمل الآن!')

# أمر إرسال رسالة التكتات
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_tickets(ctx):
    embed = discord.Embed(title="نظام الدعم الفني", description="اختر نوع التكت من القائمة أدناه للبدء.")
    await ctx.send(embed=embed, view=TicketView())

# تشغيل البوت باستخدام الـ Token من متغيرات البيئة
bot.run(os.getenv('TOKEN'))