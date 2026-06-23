require('dotenv').config();
const { Client, GatewayIntentBits, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle, PermissionsBitField, ChannelType } = require('discord.js');

const client = new Client({ 
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMembers] 
});

// ضع أرقام الرتب هنا
const SUPPORT_ROLE_IDS = ['123456789']; 

client.once('ready', () => { console.log(`البوت متصل كـ: ${client.user.tag}`); });

client.on('interactionCreate', async interaction => {
    if (interaction.isChatInputCommand() && interaction.commandName === 'ticket') {
        const channel = await interaction.guild.channels.create({
            name: `ticket-${interaction.user.username}`,
            type: ChannelType.GuildText,
            permissionOverwrites: [
                { id: interaction.guild.id, deny: [PermissionsBitField.Flags.ViewChannel] },
                { id: interaction.user.id, allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages] },
                ...SUPPORT_ROLE_IDS.map(id => ({ id, allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages] }))
            ],
        });

        const embed = new EmbedBuilder().setTitle('نظام التكت').setDescription('حياك الله، كيف نخدمك؟').setColor('Green');
        const row = new ActionRowBuilder().addComponents(
            new ButtonBuilder().setCustomId('close_ticket').setLabel('إغلاق').setStyle(ButtonStyle.Danger)
        );

        await channel.send({ content: `${interaction.user}، تم فتح التكت.`, embeds: [embed], components: [row] });
        await interaction.reply({ content: `تم فتح تكت: ${channel}`, ephemeral: true });
    }

    if (interaction.isButton() && interaction.customId === 'close_ticket') {
        await interaction.reply('سيتم إغلاق التكت...');
        setTimeout(() => interaction.channel.delete(), 3000);
    }
});

client.login(process.env.TOKEN); 