import streamlit as st

from time import sleep
from utils import *

st.header("音声データから、タイトル、ライナーノート、とジャケットを作成")

uploaded_file = st.file_uploader("音声データを選ぶ...", type=['mp3'])

segmented_summary = []

if uploaded_file is not None:
    st.write(uploaded_file.name)
    audio_file_path = uploaded_file.name
    
    # if audio_file_path.endswith("m4a"):
    #     # m4a を mp3 へ変換
    #     convert_m4a_to_mp3(audio_file_path, "audio.mp3")
    #     audio_file_path = "audio.mp3"

    # 音声データからテキストを起こす
    transcript = transcribe(uploaded_file)

    segmented_transcript = segmentation(transcript.text)

    segmented_summary = []
    for segment in segmented_transcript:
        segmented_summary.append(summarize(segment))

        sleep(5) # sleep for 5 seconds to avoid rate limit    


# segmented_summary = [
#     '会話で本を読むがカオスなので学生に見せることになり、ページの見方に苦戦している。最新のページはどこかも分からない。',
#     '中年男性のラジオネームが話題になっている。彼は生放送を経験し、現在は無職に近い状態だという。また、のぐいりのお二人が息を止めるという話題になり、歌の話も出ていた。',
#     'ドルツの会は再生回数が高く、スポンサーから商品提供もあるかも。レビューしてお金をもらえたら嬉しいけど、そういう人は少ないかも。ドルツを知った人との関係性話も多い。そんな話から、関係ない話になったけど、光る時や平家物語のアニメが好きだった。',
#     '平家物語のPVでクライマックスぽいものがある。教科書のネタバレだから結末は分かるけど、それでも感情移入する。リアルなシーンがあって光る時の歌詞が刺さる。',
#     '人があの花のストーリーを語り継ぎ、カオスなお便りが届いた中で、夫が知的な生活を送らないことが悩みとなっている。どうアドバイスすべきか考える。',
#     '夫が学ぶ姿勢を持って欲しいと思っているが、彼がどういう意味でそれを実践するかは不明。彼女には夫との会話が全て仕事、ゲーム、ポケモンに集中していて、もっと知的な話をして欲しいと思う一方で、ポケモンは十分に知的で刺激的だと反論もされている。',
#     '対戦で確率に基づくゲームなので、70％命中率の攻撃はドキドキする。しかし、100％命中率の攻撃を選べば運の要素を最小限に抑えられる。レイリゾーさんはポケモン世界大会で3連覇を達成したが、運に逆らわれて落ちてしまうこともあるため、最小限に抑えることが重要。',
#     'ポケモンバトルで新しい対策を考えることができ、バトルにおいて現実に近い要素があるため、命中率コントロールを行いマネジメントすることができるという点において、仕事に活かせているという。',
#     'ポケモンの会話が高度なマネジメントの表れと思われる。また、ポケモンには今でも未来の姿を想像している人々がいる。',
#     'ポケモンの初代151匹は、開発者のたじりさとしの少年時代の体験から生まれた。ピカチュウはアニメ化された後にブランティングされたもので、ゲームフリックで作られたポケモンである。それは、子供たちが外で遊ばなくなった時代に誕生したゲームだった。',
#     '\n\n自然や生き物との接し方がポケモンで変わると思うたじり少年。ポケモンは子供たちに影響を与え、自然との対話を促進するサービスだと考えている。株式会社ポケモンはアーティストとのコラボを積極的に行い、スカルプチャーのミュージアムなどがある。',
#     'ポケモンがアート界で注目され、グラミー賞でもカービィが取ったことで、ゲームとアートが繋がりが出てきた。常に新しい価値観を出してくれるポケモンは、過去を下げないようにしてほしい。今後、学コラボや野食家コラボなど、新しい可能性もある。',
#     '増田さん体制になってから辰里さんが出なくなり、過去の話や子供たちには関係ないことはNG。ポケモン好きのオタクたちが気にするだけ。推しポケモンはヌオウで、ドオウといういとこが茶色い。クラスではヌオウ好きと言われていた。',
#     'ヌオウの人気が上昇中で、可愛がられるようになった。ツイッターのコミュニティも盛ん。DMで可愛いポケモン紹介やおすすめ漫画を募集している。'
# ]

selected_segments_idx = [ st.checkbox(segment) for segment in segmented_summary ]

selected_segments = [ segmented_summary[i] for i, selected in enumerate(selected_segments_idx) if selected ]

#
# Output
#

def generate_output():
    note = '\n'.join(selected_segments)
    if len(note) > 0:
        title = create_title(note)
        image_text = note if len(note) < 500 else summarize(note)
        image_url = create_image(image_text)

        st.write(f'タイトル: {title}')
        st.write(f'ライナーノート:\n{note}')
        st.write(f'画像のテキスト:\n{image_text}')
        st.image(image_url)

if len(selected_segments_idx) > 0:
    st.button('生成する！', on_click=generate_output)