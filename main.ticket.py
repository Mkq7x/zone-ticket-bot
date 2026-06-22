const { Client, GatewayIntentBits, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle, PermissionsBitField, ChannelType } = require('discord.js');

// --- إعداداتك ---
const TOKEN = 'ضع_التوكين_الخاص_ببوتك_هنا';
const SUPPORT_ROLE_IDS = ['رقم_الرتبة_1', 'رقم_الرتبة_2']; // ضع أرقام الرتب هنا
// ----------------

const client = new Client({ 
    intents: [
        GatewayIntentBits.Guilds, 
        GatewayIntentBits.GuildMessages, 
        GatewayIntentBits.MessageContent, 
        GatewayIntentBits.GuildMembers
    ] 
});

client.once('ready', () => { 
    console.log(`البوت جاهز باسم: ${client.user.tag}`); 
});

client.on('interactionCreate', async interaction => {
    // منطق فتح التكت (أمر /ticket)
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

        const embed = new EmbedBuilder()
            .setDescription('حياك الله، كيف أقدر أخدمك؟')
            .setColor('Green');

        const row = new ActionRowBuilder().addComponents(
            new ButtonBuilder()
                .setCustomId('close_ticket')
                .setLabel('إغلاق التكت')
                .setStyle(ButtonStyle.Danger)
        );

        await channel.send({ content: `${interaction.user}، تم فتح التكت.`, embeds: [embed], components: [row] });
        await interaction.reply({ content: `تم فتح التكت: ${channel}`, ephemeral: true });
    }

    // منطق زر الإغلاق
    if (interaction.isButton() && interaction.customId === 'close_ticket') {
        if (!interaction.member.roles.cache.some(r => SUPPORT_ROLE_IDS.includes(r.id))) {
            return interaction.reply({ content: 'عذراً، الإدارة فقط من يمكنها إغلاق التكت!', ephemeral: true });
        }
        await interaction.reply('سيتم إغلاق التكت...');
        setTimeout(() => interaction.channel.delete(), 3000);
    }
});

client.login(TOKEN);
