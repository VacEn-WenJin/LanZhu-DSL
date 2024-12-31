from manim import *
import numpy as np

class MovingDotOnAxis(Scene):
    def construct(self):
        # 创建一个简单的直线
        line = Line(
            start=LEFT * 5,
            end=RIGHT * 5,
            color=BLUE
        )
        
        # 创建最终要显示的数轴
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color=BLUE,
            include_tip=True,
        )
        
        # 创建向上的短竖线作为刻度
        ticks = VGroup(*[
            Line(
                start=number_line.number_to_point(x) + DOWN * 0.1,
                end=number_line.number_to_point(x) + UP * 0.1,
                color=GREY
            )
            for x in range(-5, 5)
        ])
        
        # 创建坐标值标签
        labels = VGroup(*[
            MathTex(str(x)).scale(0.4).next_to(
                number_line.number_to_point(x),
                DOWN * 1.2
            )
            for x in range(-5, 6)
        ])

        # 定义关键位置和时间点 (4秒周期)
        key_points = {
            0: -2,     # 起始位置（休息地）
            0.6: -1,   # 向觅食地移动
            1.2: 2,    # 到达主要觅食地
            2.0: 2,    # 在觅食地停留
            2.4: 3,    # 短暂探索
            2.8: 0,    # 返程途中
            3.4: -2,   # 回到休息地
            4.0: -2    # 完成一天循环
        }

        # 创建获取位置的函数
        def get_position_at_time(t):
            t = t % 4  # 将时间映射到0-4秒的周期内
            for next_t in sorted(key_points.keys()):
                if t <= next_t:
                    prev_t = max([k for k in key_points.keys() if k <= t])
                    next_t = min([k for k in key_points.keys() if k >= t])
                    if prev_t == next_t:
                        return key_points[prev_t]
                    alpha = (t - prev_t) / (next_t - prev_t)
                    alpha = smooth(alpha)
                    return key_points[prev_t] + (key_points[next_t] - key_points[prev_t]) * alpha
            return key_points[0]
        
        # 创建更大的粉色动点，初始位置在休息地
        moving_dot = Dot(color=PINK, radius=0.3)
        moving_dot.move_to(line.point_from_proportion((key_points[0] + 5) / 10))
        
        # 创建点的坐标显示
        dot_symbol = Dot(color=PINK, radius=0.1)
        coord_text = MathTex("x = ").scale(0.7)
        coord_value = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            color=PINK
        ).scale(0.7)
        coord_group = VGroup(dot_symbol, coord_text, coord_value).arrange(RIGHT, buff=0.2)
        coord_group.next_to(number_line, DOWN, buff=0.5)
        
        # 创建location标签
        loc_label = Text("location", font_size=24).next_to(number_line, LEFT, buff=0.5)
        loc_final = Text("loc.", font_size=24).next_to(number_line, LEFT, buff=0.5)
        
        # 更新坐标显示的函数
        def update_coord_value(dec):
            dec.set_value(moving_dot.get_center()[0])
        coord_value.add_updater(update_coord_value)
        
        # 添加直线
        self.play(Create(line))
        
        # 点的缩放动画
        self.play(
            moving_dot.animate.scale(0.7),
            rate_func=there_and_back,
            run_time=0.3
        )

        # 第一次完整的生物活动周期
        start_time = 0
        while start_time < 4:
            target_x = get_position_at_time(start_time + 0.02)
            target_point = line.point_from_proportion((target_x + 5) / 10)
            self.play(
                moving_dot.animate.move_to(target_point),
                rate_func=linear,
                run_time=0.02
            )
            start_time += 0.02

        # 将直线转变为数轴并显示刻度值
        self.play(
            ReplacementTransform(line, number_line),
            Create(ticks),
            run_time=1.5
        )
        
        # 显示坐标值标签
        self.play(FadeIn(labels))
        
        # 显示坐标文本和location标签
        self.play(
            FadeIn(coord_group),
            Write(loc_label)
        )
        
        # 将location变为loc.
        self.play(
            ReplacementTransform(loc_label, loc_final)
        )
        
        # 点的缩小动画
        self.play(
            moving_dot.animate.scale(0.3),
            run_time=0.5
        )
        
        # 创建并显示指向箭头
        arrow = Arrow(
            start=moving_dot.get_center() + UP * 0.8,
            end=moving_dot.get_center(),
            color=BLUE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.4
        )
        self.play(Create(arrow), run_time=0.5)
        
        # 短暂停留后移除箭头
        self.wait(0.5)
        self.play(FadeOut(arrow), run_time=0.3)
        
        # 点恢复原来大小并完成一次运动周期
        self.play(
            moving_dot.animate.scale(3.33),
            run_time=0.5
        )

        # 第二次完整的生物活动周期
        start_time = 0
        while start_time < 4:
            target_x = get_position_at_time(start_time + 0.02)
            target_point = number_line.number_to_point(get_position_at_time(start_time + 0.02))
            self.play(
                moving_dot.animate.move_to(target_point),
                rate_func=linear,
                run_time=0.02
            )
            start_time += 0.02

        # 创建时间轴和相关元素
        time_line = NumberLine(
            x_range=[0, 4, 1],
            length=6,
            color=ORANGE,
            include_tip=True,
        ).shift(UP * 2.5)
        
        time_labels = VGroup(*[
            MathTex(str(x)).scale(0.4).next_to(
                time_line.number_to_point(x),
                DOWN * 0.8
            )
            for x in range(5)
        ])
        
        time_label = Text("time", font_size=24).next_to(time_line, LEFT, buff=0.5)
        t_label = MathTex("t").scale(0.8).next_to(time_line, LEFT, buff=0.5)

        # 创建时间的坐标显示
        time_coord_text = MathTex(",\\, t = ").scale(0.7)
        time_coord_value = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=False,
            color=PINK
        ).scale(0.7)
        time_coord_group = VGroup(time_coord_text, time_coord_value).arrange(RIGHT, buff=0.1)
        
        # 创建组合的表达式组
        combined_group = VGroup(coord_group, time_coord_group).arrange(RIGHT, buff=0.1)
        combined_group.next_to(number_line, DOWN, buff=0.5)

        # 创建一个全局变量来存储当前时间值
        self.current_t = 0

        # 修改后的更新函数
        def update_time_value(dec):
            dec.set_value(self.current_t)
        
        time_coord_value.add_updater(update_time_value)

        # 显示时间轴和标签
        self.play(
            Create(time_line),
            FadeIn(time_labels),
            Write(time_label)
        )
        
        # 将time转换为t
        self.play(
            ReplacementTransform(time_label, t_label)
        )

        # 移动原有坐标显示并显示时间坐标
        self.play(
            coord_group.animate.move_to(combined_group[0].get_center()),
            FadeIn(time_coord_group)
        )

        # 第三次完整的生物活动周期，同时展示时间
        start_time = 0
        current_time_dot = None
        while start_time < 4:
            # 创建新的时间点
            new_time_dot = Dot(color=PINK, radius=0.2)
            new_time_dot.move_to(time_line.number_to_point(start_time))
            
            # 如果存在旧的时间点，则淡出
            if current_time_dot is not None:
                self.remove(current_time_dot)
            
            # 显示新的时间点
            self.add(new_time_dot)
            current_time_dot = new_time_dot
            
            # 更新位置
            target_x = get_position_at_time(start_time + 0.02)
            target_point = number_line.number_to_point(target_x)
            
            # 更新当前时间值
            self.current_t = start_time + 0.02
            
            # 同步移动点和时间
            self.play(
                moving_dot.animate.move_to(target_point),
                new_time_dot.animate.move_to(time_line.number_to_point(start_time + 0.02)),
                rate_func=linear,
                run_time=0.02
            )
            
            start_time += 0.02

        # 等待一下并结束
        self.wait()